import json
from error_messages import ErrorMessages
# MSG_ACC_NUM_ERROR = 'Account number is not available!!! Please logout and login again.'

class AccountManager:

    def __init__(self):
        self.__accounts = {}
        self.__account_number = ''
        self.__load_accounts()

    def __load_accounts(self):
        try:
            with open('account_data.json', 'r') as f:
                data = json.load(f)
                for acc_num, acc_data in data.items():
                    self.__accounts[acc_num] = {
                        'pin': acc_data['pin'],
                        'balance': acc_data['balance']
                    }
        except FileNotFoundError:
            pass

    def authenticate(self, account_number, pin):
        account = self.get_account(account_number)
        if account and account['pin'] == pin:
            self.__account_number = account_number
            return True
        return False

    def __save_accounts(self):
        data = {acc_num: {'pin': acc_data['pin'], 'balance': acc_data['balance']}
                for acc_num, acc_data in self.__accounts.items()}
        with open('account_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def add_account(self, account_number, pin, balance=0):
        self.__accounts[account_number] = {'pin': pin, 'balance': balance}
        self.__save_accounts()

    def get_account(self, account_number):
        return self.__accounts.get(account_number)
    
    def __validate_amount(self, amount):
        if amount <= 0:
            return ErrorMessages.INVALID_AMOUNT
        return None
    
    def __validate_account(self):
        if not self.__account_number:
            return ErrorMessages.ACCOUNT_NOT_SET
        return None
    
    def __validate_transaction(self, transaction_type, amount):
        error_message = self.__validate_amount(amount)
        if error_message:
            return error_message

        error_message = self.__validate_account()
        if error_message:
            return getattr(ErrorMessages, f'{transaction_type.upper()}_ERROR')

    def __execute_withdraw(self, account, amount):
        if account['balance'] >= amount:
            account['balance'] -= amount
            self.__save_accounts()
            return f'Withdrawal successful: ${amount}'
        else:
            return ErrorMessages.INSUFFICIENT_FUNDS

    def __execute_deposit(self, account, amount):
        account['balance'] += amount
        self.__save_accounts()
        return f'Deposit successful: ${amount}'
    
    def __execute_transaction(self, account, transaction_type, amount):
        if transaction_type == 'withdraw':
            return self.__execute_withdraw(account, amount)
        elif transaction_type == 'deposit':
            return self.__execute_deposit(account, amount)
        else:
            return ErrorMessages.INVALID_TRANSACTION
        
    def __perform_transaction(self, transaction_type, amount):
        error_message = self.__validate_transaction(transaction_type, amount)
        if error_message:
            return error_message

        account = self.get_account(self.__account_number)
        if not account:
            return ErrorMessages.ACCOUNT_NOT_FOUND

        return self.__execute_transaction(account, transaction_type, amount)
    
    def check_balance(self):
        if self.__account_number != '':
            account = self.get_account(self.__account_number)
            return f"Your account balance is: ${account['balance']}"
        else:
            return ErrorMessages.ACCOUNT_NOT_SET
        
    def withdraw_money(self, money_to_withdraw):
        return self.__perform_transaction('withdraw', money_to_withdraw)

    def deposit_money(self, money_to_deposit):
        return self.__perform_transaction('deposit', money_to_deposit)
        
    # def withdraw_money(self, money_to_withdraw):
    #     if money_to_withdraw > 0:
    #         if self.account_number != '':
    #             account = self.get_account(self.account_number)
    #             if account:
    #                 if account['balance'] >= money_to_withdraw:
    #                     account['balance'] -= money_to_withdraw
    #                     self.save_accounts()
    #                     return f"Withdrawal successful: ${money_to_withdraw}"
    #                 else:
    #                     return 'Error: Insufficent funds, enter valid amount.'
    #         else:
    #             return 'Withdraw Error: ' + MSG_ACC_NUM_ERROR
    #     else:
    #         return 'Please enter valid amount!!!'

    # def deposit_money(self, money_to_deposit):
    #     if money_to_deposit > 0:
    #         if self.account_number != '':
    #             account = self.get_account(self.account_number)
    #             if account:
    #                 account['balance'] += money_to_deposit
    #                 self.save_accounts()
    #                 return f"Deposit successful: ${money_to_deposit}"
    #         else:
    #             return 'Deposit Error: ' + MSG_ACC_NUM_ERROR
    #     else:
    #         return 'Please enter valid amount!!!'