import hashlib
import random
import string
from database import connect_to_database


# ENCRYPT and VERIFY PIN
def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def verify_pin(input_pin, store_hash):
    return hash_pin(input_pin) == store_hash    
    
# DB and TABLE INITIALIZE
def inialize_tables():
    connection = connect_to_database()
    if not connection:
        return False
    try:
        cursor = connection.cursor()
        
        create_accounts_table = """
        CREATE TABLE IF NOT EXISTS accounts(
            account_number varchar(50) primary key,
            name varchar(100) not null,
            pin varchar(64) not null,
            balance decimal(15,2) default 0.00,
            created_at timestamp default current_timestamp
        );
        """
        
        create_audit_table = """
        CREATE TABLE IF NOT EXISTS audit(
            id serial primary key,
            account_number varchar(50),
            holder_name varchar(100),
            action varchar(100) not null,
            amount decimal(15,2) default 0.00,
            timestamp timestamp default current_timestamp,
            FOREIGN KEY (account_number) references accounts(account_number) 
            ON DELETE CASCADE
        );
        """
        
        cursor.execute(create_accounts_table)
        cursor.execute(create_audit_table)
        
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as error:
        print(f"Error initializing table: {error}")
        return False


# ACCOUNT CLASS
class Account:
    def __init__(self, name="", pin="", account_number=""):
        self.__account_number = (
            account_number if account_number else self.__generate_account_number()
        )
        self.__name = name
        self.__pin = hash_pin(pin) if pin else ""
        self.__balance = 0.0
        
    @staticmethod
    def __generate_account_number():
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
    # GETTERS
    def get_account_number(self):
        return self.__account_number
    
    def get_name(self):
        return self.__name
        
    def get_pin_hash(self):
        return self.__pin
    
    def get_balance(self):
        return self.__balance
    
    # SETTERS
    def set_name(self, name):
        self.__name = name
            
    def set_pin_hash(self, pin):
        self.__pin = hash_pin(pin)
        
    def set_balance(self, balance):
        self.__balance = balance
        
    # UTILITY
    def deposit(self, amount):
        if amount <= 0:
            return False
        self.__balance += amount
        return True
    
    def withdraw(self, amount):
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True
        
    # Database CRUD
    @classmethod
    def load_from_db(cls, account_number, pin):
        connection = connect_to_database()
        if not connection:
            return None
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT account_number, name, pin, balance FROM accounts WHERE account_number=%s",
                (account_number,),
            )
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                stored_pin_hash = result[2]
                if verify_pin(pin, stored_pin_hash):
                    account = cls(result[1], pin, result[0])
                    account.set_balance(float(result[3]))
                    return account
            return None
        except Exception as error:
            print(f"Error loading account: {error}")
            return None
         
    def save_to_db(self):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO accounts (account_number, name, pin, balance)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (account_number)
                DO UPDATE SET name = %s, pin = %s ,balance=%s
                """,
                (
                    self.__account_number, 
                    self.__name, 
                    self.__pin, 
                    self.__balance,
                    self.__name, 
                    self.__pin, 
                    self.__balance,
                ),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as error:
            print(f"Error creating/updating account: {error}")
            return False
     
    def delete_from_db(self):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM accounts WHERE account_number=%s",
                (self.__account_number,),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as error:
            print(f"Error closing account: {error}")
            return False
         

# AUDIT CLASS
class Audit:
    @staticmethod
    def log_action(account_number, holder_name, action, amount=0.0):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO audit (account_number, holder_name, action, amount) VALUES (%s, %s, %s, %s)",
                (account_number, holder_name, action, amount),
            )
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as error:
            print(f"Error auditing actions: {error}")
            return False
            
    @staticmethod
    def get_single_audit_log(account_number):
        connection = connect_to_database()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            cursor.execute(
               """
               SELECT id, holder_name, action, amount, timestamp
               FROM audit
               WHERE account_number = %s
               ORDER BY timestamp DESC
               """,
               (account_number,)  
            )
            results = cursor.fetchall()  
            cursor.close()
            connection.close()
            
            logs = []
            for row in results:
                logs.append({
                    "id": row[0],
                    "holder_name": row[1],
                    "action": row[2],
                    "amount": row[3],
                    "timestamp": row[4],
                })
            return logs
        except Exception as error:
            print(f"Error logging {account_number} actions: {error}")
            return []
            
    @staticmethod
    def get_all_audit_log():
        connection = connect_to_database()
        if not connection:
            return []
        try:
            cursor = connection.cursor()
            cursor.execute(
               """
               SELECT id, holder_name, action, amount, timestamp
               FROM audit
               ORDER BY timestamp DESC
               """
            )
            results = cursor.fetchall()  # Fixed: fetchall instead of fetchone
            cursor.close()
            connection.close()
            
            logs = []
            for row in results:
                logs.append({
                    "id": row[0],
                    "holder_name": row[1],
                    "action": row[2],
                    "amount": row[3],
                    "timestamp": row[4],
                })
            return logs
        except Exception as error:
            print(f"Error logging all audit actions: {error}")
            return []
    
    @staticmethod
    def clear_single_audit_log(account_number):
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM audit WHERE account_number=%s", (account_number,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as error:
            print(f"Error clearing {account_number} actions: {error}")
            return False
            
    @staticmethod
    def clear_all_audit_log():
        connection = connect_to_database()
        if not connection:
            return False
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM audit")
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as error:
            print(f"Error clearing all audit actions: {error}")
            return False


# BANK SYSTEM CLASS 
class BankSystem:
    def __init__(self):
        inialize_tables()

    def create_account(self, name, pin):
        account = Account(name, pin)
        if account.save_to_db():
            Audit.log_action(
                account.get_account_number(), account.get_name(), "Account Create", 0.0
            )
            return account
        return None
        
    def read_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if account:
            Audit.log_action(account_number, account.get_name(), "Details checked", 0.0)
            return account
        return None
    
    def update_account(self, account):
        return account.save_to_db()
    def delete_account(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if account:
            success = account.delete_from_db()
            if success:
                Audit.log_action(account_number, account.get_name(), "Account closed", 0.0)
                return True
        return False      
    
    def deposit(self, account_number, pin, amount):
        account = Account.load_from_db(account_number, pin)
        if account and account.deposit(amount):
            account.save_to_db()  # Persist balance update
            Audit.log_action(
                account_number, account.get_name(), "Amount Deposited", amount
            )
            return True
        return False      
    
    def withdraw(self, account_number, pin, amount):
        account = Account.load_from_db(account_number, pin)
        if account and account.withdraw(amount):
            account.save_to_db()  # Persist balance update
            Audit.log_action(
                account_number, account.get_name(), "Amount Withdrawn", amount
            )
            return True
        return False   
    
    def get_account_balance(self, account_number, pin):
        account = Account.load_from_db(account_number, pin)
        if account:
            Audit.log_action(
                account_number, account.get_name(), "Balance Checked", 0.0
            )
            return account.get_balance()
        return None
    
    def get_single_audit_logs(self, account_number):
        return Audit.get_single_audit_log(account_number)     
    
    def get_all_audit_logs(self):
        return Audit.get_all_audit_log()
    
    def clear_single_audit_logs(self, account_number):
        return Audit.clear_single_audit_log(account_number)     
        
    def clear_all_audit_logs(self):
        return Audit.clear_all_audit_log()
        
        
# VALID AMOUNT INPUT
def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid amount in numbers.")
            
            
# CLI MENU FUNCTIONS

# CREATE ACCOUNT CLI FUNCTION
def create_account_cli(bank):
    print("=" * 40)
    print(" CREATE NEW ACCOUNT")
    print("=" * 40)
    name = input("Enter your Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        input("Press Enter to continue...")
        return
        
    pin = input("Enter 4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be a 4-digit number.")
        input("Press Enter to continue...")
        return
    
    confirm_pin = input("Confirm your PIN: ").strip()
    if pin != confirm_pin:
        print("PINs do not match.")
        input("Press Enter to continue...")
        return

    account = bank.create_account(name, pin)
    if account:
        print(f"\nAccount successfully created!")
        print(f"Account Number: {account.get_account_number()}")
        print(f"Save your Account Number and PIN securely.")
    else:
        print(f"\nAccount could not be created, try again!")
        
    input("Press Enter to continue...")

#LOGED IN FUNCTION
def check_balance_cli(bank,account,pin):
    print("=" * 40)
    print("CURRENT ACCOUNT BALANCE")
    print("=" * 40)
    balance = bank.get_account_balance(account.get_account_number(),pin)
    if balance is not None:
        print(f"Current Balance: Rs{balance:.2f}")
    else:
        print("Error checking balance ,try again.")
          
    input("Press Enter to continue...")

def deposit_money_cli(bank,account,pin):
    print("=" * 40)
    print("DEPOSIT MONEY")
    print("=" * 40)
    
    amount =get_valid_amount("Enter Deposit Amount : Rs")
    
    if bank.deposit(account.get_account_number(),pin,amount):
        print(f"Rs{amount:.2f} successfully Deposited.")
        balance=bank.get_account_balance(account.get_account_number(),pin)    
        if balance is not None:
            print(f"Current Balance: Rs{balance:.2f}")
    else:
        print("Error depositing balance ,try again.")     
    input("Press Enter to continue...")

def withdraw_money_cli(bank,account,pin):
    print("=" * 40)
    print("Withdraw MONEY")
    print("=" * 40)
    amount =get_valid_amount("Enter Withdraw Amount : Rs")
    if bank.withdraw(account.get_account_number(),pin,amount):
        print(f"Rs{amount:.2f} successfully withdrawn.")
        balance=bank.get_account_balance(account.get_account_number(),pin)    
        if balance is not None:
            print(f"New Balance: Rs{balance:.2f}")
    else:
        print("Error depositing balance ,try again.")     
    input("Press Enter to continue...")

def transaction_history_cli(bank,account,pin):
    print("=" * 40)
    print("USER TRANSACTION HISTORY")
    print("=" * 40)
    logs = bank.get_single_audit_logs(account.get_account_number())
    if not logs:
        print("No Transaction Found.")
    else:
        for log in logs:
            print(f"log['timestamp'] {log['action']} - Rs{log['amount']:.2f} By: {log['holder_name']}")
    input("Press Enter to continue...")

def update_account_info_cli(bank,account,pin):
    print("=" * 40)
    print("UPDATE ACCOUNT INFO")
    print("=" * 40)
    new_name = input("Enter your Name: ").strip()
    if new_name:
        account.set_name(new_name)
        if bank.update_account(account):
            Audit.log_action(
                account.get_account_number(),
                account.get_name(),
                "Account info upated",
                0.0,
            )
            print("Name updated successfully")
        else:
            print("Error updating Name")
    else:
        print("No Changes made.")
    input("Press enter to contiinue...")

def change_pin_logout_cli(bank,account,pin):
    print("=" * 40)
    print("CHANGE ACCOUNT PIN")
    print("=" * 40)
    old_pin=input("Enter current PIN").strip()
    if old_pin != pin:
        print("Incorrect currect pin.")
        input("Press enter to contiinue...")
        return False
    
    new_pin = input("Enter 4 digit new PIN: ").strip()
    if len(new_pin) != 4 or not new_pin.isdigit():
        print("PIN must be a 4-digit number.")
        input("Press Enter to continue...")
        return
    
    confirm_pin = input("Confirm your PIN: ").strip()
    if new_pin != confirm_pin:
        print("PINs do not match.")
        input("Press Enter to continue...")
        return False
    account.set_pin_hash(new_pin)
    if bank.update_account(account):
            Audit.log_action(
                account.get_account_number(),
                account.get_name(),
                "PIN change (Auto Logout)",
                0.0,
            )
            print("Pin update  successfuly. You will be logged out")
            input("Press enter to contiinue...")
            return True 
    print("Error updating PIN, try again.")
    input("Press enter to contiinue...")
    return False

def delete_account_cli(bank,account,pin):
    print("=" * 40)
    print("CLOASE ACCOUNT")
    print("=" * 40)
    confirm=input("Are you sure, you  want to delete this account? (yes/no)").strip().lower()
    if confirm != "yes":
        print("Account deletion cancelled.")
        input("Press enter to contiinue...")
        return False
    
    re_pin = input("re-enter you PIN to confirm: ").strip()
    if re_pin !=pin:
        print("PIN did not match. Account not closed ")
        input("Press Enter to continue...")
        return
    
    if bank.delete_account(account.get_account_number(),pin):
        print("Account closed succefully")
        input("Press Enter to continue...")
        return True
   
    print("Error closing account, try again.")
    input("Press enter to continue...")
    return False

# LOGIN ACCOUNT CLI FUNCTION
def login_account_cli(bank):
    print("=" * 40)
    print(" CREATE NEW ACCOUNT")
    print("=" * 40)
    account_number = input("Enter your Account Number: ").strip()
    if not account_number:
        print("Account Number cannot be empty/ignore.")
        input("Press Enter to continue...")
        return
        
        
    pin = input("Enter 4-digit PIN: ").strip()
    account=bank.read_account(account_number,pin)
    if not account:
        print("Wrong creadientials.")
        input("Press Enter to continue...")
        return
    
    
    while True:
        print("=" * 40)
        print(f"WELCOME, {account.get_name()} !")
        print(f"ACCOUNT NUMBER: {account.get_account_number()}!")
        print("=" * 40)
        
        print("1. Current Balance")
        print("2. Deposit Balance")
        print("3. Withdraw Balance")
        print("4. Transaction History")
        print("5. Update Account Info")
        print("6. Update Account Pin")
        print("7. Close Account")
        print("8. Logout")
        print("=" * 40)
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            check_balance_cli(bank,account,pin)
        elif choice == "2":
            deposit_money_cli(bank,account,pin)
        elif choice == "3":
            withdraw_money_cli(bank,account,pin)
        elif choice == "4":
            transaction_history_cli(bank,account,pin)
        elif choice == "5":
           update_account_info_cli(bank,account,pin)
        elif choice == "6":
            change_pin_logout_cli(bank,account,pin)
            break
        elif choice == "7":
            if delete_account_cli(bank,account,pin):
                break
        elif choice == "8":
            # print("Thank you so much for using our services, do visit again!")
            break
        else:
            print("Invalid choice, try again")
            input("Press Enter to continue...")
            
# MAIN MENU OF CLI
def main_menu_cli():
    bank = BankSystem()
    while True:
        print("=" * 40)
        print("BANK MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. New Account")
        print("2. Login Account")
        print("5. Exit")
        print("=" * 40)
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            create_account_cli(bank)
        elif choice == "2":
            login_account_cli(bank)
        elif choice == "5":
            print("Thank you so much for using our services, do visit again!")
            break
        else:
            print("Invalid choice, try again")
            input("Press Enter to continue...")
            
            
if __name__ == "__main__":
    main_menu_cli()