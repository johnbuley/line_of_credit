from datetime import date,  timedelta

class Account(object):
    
    def __init__(self, name, apr, credit_limit, current_date, bank):
        """ Create a new account object """
        
        # These fields are just used for record-keeping
        self.name = name
        self.open_date = current_date
        self.credit_limit = credit_limit
        
        self.last_statement_date = current_date
        self.apr = apr
        self.credit_remaining = credit_limit
        self.outstanding_principal = 0.0
        self.interest_owed = 0.0
        self.transaction_history = []
        self.current_statement = []
        # Need to store bank so that bank.get_next_transaction_id() can be called.
        self.bank = bank
        
        
    def request_draw(self, amount, current_date):
        """ Draw on credit line """
        
        # Check that sufficient credit is available for amount requested.
        if amount < self.credit_remaining:
            self._draw(amount, current_date)
            return 1
        else:
            print('Insufficient credit available')
            return 0
            
            
    def make_payment(self, amount, current_date):
        """ Pay down balance """

        # Check that amount is not more than is owed
        if amount < self.outstanding_principal + self.interest_owed:
            self._pay(amount, current_date)
            return 1
        else:
            print('Overpayment')
            return 0
            
    
    def calc_interest(self, current_date):
        """ Return the balance payable """
        
        interest = 0
        
        for record in self.current_statement:
            # Creating a Record object with named fields would make this cleaner that just using a tuple.  
            # As it stands, record[1] is the amount of the draw/payment, record[3] is 1 for a draw, -1 for 
            # a payment, and record[2] is the date of the transaction.
            interest += self.apr*record[1]*record[3]*(current_date-record[2]).days/365
        
        return interest
        
        
    def close_statement(self, current_date):
        """ 30-day calculations """
        
        interest = self.calc_interest(current_date)
        self.interest_owed += interest
        self.credit_remaining -= interest
        
        # Clear statement
        self.current_statement = []
        
        # If there is outstanding principal, add to the new statement a new transaction with a
        # 'null' (-1) transaction_id.  This synthetically represents a new draw on this date,
        # since the previous balance was swept off the statement.
        if self.outstanding_principal > 0:
            record = [-1, self.outstanding_principal, current_date, 1]
            self.current_statement.append(record)
        
        self.last_statement_date = current_date
        
        return interest
        
        
    def get_transaction_history(self):
        """ Return transaction history """
        
        return self.transaction_history


    def _draw(self, amount, current_date):
        """ Internal method for drawing on credit line """
        
        self.credit_remaining -= amount
        self.outstanding_principal += amount
        
        record = [self.bank.get_next_transaction_id(), amount, current_date, 1]
        
        self.transaction_history.append(record)
        self.current_statement.append(record)
        
        
    def _pay(self, amount, current_date):
        """ Internal method for paying down balance """
        
        # If amount is greater than interest owed, then a principal payment will be made as well.
        if amount > self.interest_owed:
            amount_remaining = amount
            if self.interest_owed > 0:
                amount_remaining = self._pay_interest(amount_remaining, current_date)
            self._pay_principal(amount_remaining, current_date)
        # If amount is not greater than interest owed, then only an interest payment will be made.
        else:
            self._pay_interest(amount, current_date)
        return 1
        
        
    def _pay_interest(self, amount, current_date):
        """ Internal method for an interest payment """
        
        interest_paid = min(amount, self.interest_owed)
        
        amount -= interest_paid
        self.interest_owed -= interest_paid
        self.credit_remaining += interest_paid
        
        record = [self.bank.get_next_transaction_id(), interest_paid, current_date, 0]
        self.transaction_history.append(record)
        self.current_statement.append(record)
        
        return amount
        
        
    def _pay_principal(self, amount, current_date):
        """ Internal method for a principal payment """
        
        self.outstanding_principal -= amount
        self.credit_remaining += amount
        
        record = [self.bank.get_next_transaction_id(), amount, current_date, -1]
        self.transaction_history.append(record)
        self.current_statement.append(record)



class Bank(object):
    
    def __init__(self, apr, current_date):
        """ Construct Bank object """
        
        self.apr = apr
        self.current_date = current_date
        self.accounts = dict()
        self.default_credit_limit = 1000
        
        self.next_account_id = -1
        self.next_transaction_id = -1
        
        
    def create_account(self, name):
        """ Create account, return account id """
        
        self.next_account_id += 1
        
        self.accounts[self.next_account_id] = \
            Account(name, self.apr, self.default_credit_limit, self.current_date, self)
        
        return self.next_account_id
        
    
    def request_draw(self, id, amount):
        """ Request draw on specified account """
        
        if id in self.accounts:
            return self.accounts[id].\
                                    request_draw(amount, self.current_date)
        else:
            print('Unknown account id')
            return 0
            
            
    def make_payment(self, id, amount):
        """ Make payment on specified account """
        
        if id in self.accounts:
            return self.accounts[id].make_payment(amount, self.current_date)
        else:
            print('Unknown account id')
            return 0
            
            
    def request_customer_history(self, id):
        """ Return transaction history of account """
            
        if id in self.accounts:
            return self.accounts[id].get_transaction_history()
        else:
            print('Unknown account id')
            return None
            
    def print_account_summary(self, id):
        """ Return account summary object """
    
        if id in self.accounts:
            account = self.accounts[id]
            print('Account Id: {0}'.format(id))
            print('Account Name: {0}'.format(account.name))
            print('Credit Limit: ${0:.2f}'.format(account.credit_limit))
            print('Balance: ${0:.2f}'.format(account.outstanding_principal+account.interest_owed))
            print('--Outstanding Principal: ${0:.2f}'.format(account.outstanding_principal))
            print('--Interest Owed: ${0:.2f}'.format(account.interest_owed))
            print('Credit Remaining: ${0:.2f}'.format(account.credit_remaining))
            print()
        else:
            print('Unknown account id')
            
        
    def increment_date(self):
        """ Increment date """
    
        self.current_date += timedelta(1)
        
        for account_id in self.accounts:
            # Check whether the new date triggers a statement close in any account
            if (self.current_date - self.accounts[account_id].last_statement_date).days == 30:
                self.accounts[account_id].close_statement(self.current_date)
                
                
    def advance_date(self, days):
        """ Increment current_date <days> times """
                
        for i in range(days):
            self.increment_date()
            
    def _get_account(self, id):
        """ Used for testing """
        
        if id in self.accounts:
            return self.accounts[id]
        else:
            print('Account id not found')
            return None
            
    def get_next_transaction_id(self):
        """ Returns next unique transaction id """
                
        self.next_transaction_id += 1
        return self.next_transaction_id    
        
        
        
        
        
        
        
        
        
        
        
