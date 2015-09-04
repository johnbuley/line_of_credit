from line_of_credit import Bank
from datetime import date

if __name__ == '__main__':
    
    bank = Bank(.35, date.today())
    
    id1 = bank.create_account('Scenario 1')
    id2 = bank.create_account('Scenario 2')
    
    bank.request_draw(id1, 500)
    bank.request_draw(id2, 500)
    bank.advance_date(15)
    
    bank.make_payment(id2, 200)
    bank.advance_date(10)
    
    bank.request_draw(id2, 100)
    bank.advance_date(5)
    
    print()
    print('SCENARIO 1 AT 30 DAYS')
    bank.print_account_summary(id1)
    print('SCENARIO 2 AT 30 DAYS')
    bank.print_account_summary(id2)
    
    bank.advance_date(30)
    
    print('SCENARIO 1 AT 60 DAYS')
    bank.print_account_summary(id1)
    print('SCENARIO 2 AT 60 DAYS')
    bank.print_account_summary(id2)
