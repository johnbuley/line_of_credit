Description of functionality is found in discussion.txt
An example is found in test.py

Usage:

class Bank

  Methods:
    Bank(apr, current_date)			constructor

    create_account(name)			creates account and returns unique
						<id>
    
    request_draw(id,amount)			requests a draw of <amount> on account
						<id>

    make_payment(id,amount)			attempts payment of <amount> on account
						<id>

    request_customer_history(id)		returns transaction history for account
						<id> as list

    print_account_summary(id)			prints summary of account <id>

    increment_date()				increments current_date by 1

    advance_date(days)				calls increment_date() <days> times

    get_next_transaction_id()			returns new unique transaction id


class Account

  Methods:
    Account(name,apr,credit_limit,		returns new Account for customer
            current_date,bank)			<name> with passed parameters

    request_draw(amount,current_date)		attempts draw of <amount>

    make_payment(amount,current_date)		attemps payment of <amount>

    calc_interest(current_date)			calculates interest on outstanding
						principal on <current_date>

    close_statement(current_date)		calculates interest, updates balance,
						clears statement, rolls over
						outstanding principal

    get_transaction_history()			returns transaction history as list