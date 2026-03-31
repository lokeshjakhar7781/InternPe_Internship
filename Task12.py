import random
from datetime import datetime
class Account:
    def __init__(self, account_number, account_holder_name, initial_balance=0.0):
        self.account_number = account_number
        self.account_holder_name = account_holder_name
        self.balance = initial_balance
        self.transaction_history = []
        self._log_transaction(f"Account created with initial deposit: ${initial_balance:.2f}")
    def _log_transaction(self, description):
        """Helper method to log transactions with a timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"[{timestamp}] {description}")
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction(f"Deposited: ${amount:.2f}")
            return True, f"Success! ${amount:.2f} deposited. New balance: ${self.balance:.2f}"
        return False, "Deposit amount must be greater than zero."
    def withdraw(self, amount):
        if amount <= 0:
            return False, "Withdrawal amount must be greater than zero."
        if amount > self.balance:
            return False, "Error: Insufficient funds!"
        self.balance -= amount
        self._log_transaction(f"Withdrew: ${amount:.2f}")
        return True, f"Success! ${amount:.2f} withdrawn. New balance: ${self.balance:.2f}"
    def check_balance(self):
        return self.balance
    def get_transaction_history(self):
        return self.transaction_history
class User:
    def __init__(self, name):
        self.name = name
        self.account = None  
    def assign_account(self, account):
        """Links an Account object to the User."""
        self.account = account
class Bank:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.users = {}  
    def generate_account_number(self):
        """Generates a unique 5-digit account number."""
        while True:
            acc_num = str(random.randint(10000, 99999))
            if acc_num not in self.users:
                return acc_num
    def create_account(self, user_name, initial_deposit):
        if initial_deposit < 0:
            return None, "Error: Initial deposit cannot be negative."
        acc_num = self.generate_account_number()
        new_account = Account(acc_num, user_name, initial_deposit)
        new_user = User(user_name)
        new_user.assign_account(new_account)
        self.users[acc_num] = new_user
        return acc_num, f"Account created successfully! Your Account Number is: {acc_num}"
    def get_account(self, acc_num):
        """Retrieves the account object if the account number exists."""
        user = self.users.get(acc_num)
        if user:
            return user.account
        return None
def main():
    bank = Bank("Global Python Bank")
    while True:
        print(f"\n{'='*40}")
        print(f"🏦 Welcome to {bank.bank_name} 🏦")
        print(f"{'='*40}")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")
        print(f"{'='*40}")
        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            name = input("Enter your full name: ")
            try:
                deposit = float(input("Enter initial deposit amount: $"))
                acc_num, message = bank.create_account(name, deposit)
                print("\n✅", message)
            except ValueError:
                print("\n❌ Error: Please enter a valid numerical amount.")
        elif choice == '2':
            acc_num = input("Enter your Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                try:
                    amount = float(input("Enter amount to deposit: $"))
                    success, message = account.deposit(amount)
                    print("\n✅" if success else "\n❌", message)
                except ValueError:
                    print("\n❌ Error: Please enter a valid numerical amount.")
            else:
                print("\n❌ Error: Account not found.")
        elif choice == '3':
            acc_num = input("Enter your Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                try:
                    amount = float(input("Enter amount to withdraw: $"))
                    success, message = account.withdraw(amount)
                    print("\n✅" if success else "\n❌", message)
                except ValueError:
                    print("\n❌ Error: Please enter a valid numerical amount.")
            else:
                print("\n❌ Error: Account not found.")
        elif choice == '4':
            acc_num = input("Enter your Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                print(f"\n💰 Current Balance for {account.account_holder_name}: ${account.check_balance():.2f}")
            else:
                print("\n❌ Error: Account not found.")
        elif choice == '5':
            acc_num = input("Enter your Account Number: ")
            account = bank.get_account(acc_num)
            if account:
                print(f"\n📜 Transaction History for {account.account_holder_name}:")
                for transaction in account.get_transaction_history():
                    print("  -", transaction)
            else:
                print("\n❌ Error: Account not found.")
        elif choice == '6':
            print("\n👋 Thank you for banking with us. Have a great day!")
            break
        else:
            print("\n❌ Invalid choice. Please select an option from 1 to 6.")
if __name__ == "__main__":
    main()