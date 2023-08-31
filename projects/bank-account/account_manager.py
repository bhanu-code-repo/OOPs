import json
from error_messages import ErrorMessages
MSG_ACC_NUM_ERROR = 'Account number is not available!!! Please logout and login again.'

class AccountManager:

    def __init__(self):
        self.accounts = {}
        self.account_number = ''
        self.load_accounts()

    def load_accounts(self):
        try:
            with open('account_data.json', 'r') as f:
                data = json.load(f)
                for acc_num, acc_data in data.items():
                    self.accounts[acc_num] = {
                        'pin': acc_data['pin'],
                        'balance': acc_data['balance']
                    }
        except FileNotFoundError:
            pass

    def authenticate(self, account_number, pin):
        account = self.get_account(account_number)
        if account and account['pin'] == pin:
            self.account_number = account_number
            return True
        return False

    def save_accounts(self):
        data = {acc_num: {'pin': acc_data['pin'], 'balance': acc_data['balance']}
                for acc_num, acc_data in self.accounts.items()}
        with open('account_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def add_account(self, account_number, pin, balance=0):
        self.accounts[account_number] = {'pin': pin, 'balance': balance}
        self.save_accounts()

    def get_account(self, account_number):
        return self.accounts.get(account_number)
    
    def validate_amount(self, amount):
        if amount <= 0:
            return 'Please enter a valid amount!!!'
        return None
    
    def validate_account(self):
        if not self.account_number:
            return 'Error: Account number is not set.'
        return None

    def check_balance(self):
        if self.account_number != '':
            account = self.get_account(self.account_number)
            return f"Your account balance is: ${account['balance']}"
        else:
            return 'Balance Check Error: ' + MSG_ACC_NUM_ERROR
    def withdraw_money(self, money_to_withdraw):
        if money_to_withdraw > 0:
            if self.account_number != '':
                account = self.get_account(self.account_number)
                if account:
                    account['balance'] -= money_to_withdraw
                    self.save_accounts()
                    return f"Withdrawal successful: ${money_to_withdraw}"
            else:
                return 'Withdraw Error: ' + MSG_ACC_NUM_ERROR
        else:
            return 'Please enter valid amount!!!'

    def deposit_money(self, money_to_deposit):
        if money_to_deposit > 0:
            if self.account_number != '':
                account = self.get_account(self.account_number)
                if account:
                    account['balance'] += money_to_deposit
                    self.save_accounts()
                    return f"Deposit successful: ${money_to_deposit}"
            else:
                return 'Deposit Error: ' + MSG_ACC_NUM_ERROR
        else:
            return 'Please enter valid amount!!!'