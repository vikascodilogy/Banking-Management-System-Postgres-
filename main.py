import hashlib
import random
import string
from database import connect_to_database


# ENCRYPT and VERIFY PIN
def __hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdiget()

def __verify_pin(input_pin,store_hash):
    return __hash_pin(input_pin)==store_hash    
    
#DB and TABLE INITIALIZE
def inialize_tables():
    connection=connect_to_database()
    if not connection:
        return False
    try:
        cursor=connection.cursor()
        
        create_accounts_table="""
        CREATE TABLE IF NOT EXISTS accounts(
            account_number varchar(50) primary key,
            name varchar(100) not null,
            pin varchar(64) not null,
            balance decimal(15,2) default 0.00,
            created_at timestamp default current_timestamp
        );
        """
        
        create_audit_table="""
                CREATE TABLE IF NOT EXISTS audit(
                    id serial primary key,
                    account_number varchar(50),
                    holder_name varchar(100),
                    action varchar(100) not null,
                    amount decimal(15,2) default 0.00,
                    timestamp timestamp default current_timestamp,
                    FOREIGN KEY (account_number) references accounts(account_number)
        );
        """
        
        cursor.execute(create_accounts_table)
        cursor.execute(create_audit_table)
        
        connection.commit()
        cursor.close()
        return True
                
        
    except Exception as error:
        print(f"Error initializing table: {error}")
        return False


#ACCOUNT CLASS
class Account:
    def __init__(self,name="",pin="",account_number=""):
        self.account_number=(
            account_number if account_number else self.__generate_account_number()
        )
        self.__name=name
        self.__pin=__hash_pin(pin)
        self.__balance=0.0
        
    @staticmethod
    def __generate_account_number():
        return"".join(random.choices(string.ascii_uppercase + string.digits,k=10))
        
        
    # GETTERS
    def get_account_number(self):
        return self.__account_number
    
    def get_name(self):
        return self.__name
        
    def get_pin_hash(self):
        return self.__pin
    
    def get_balance(self):
        return self.__balance
    
    
    # SETERS
    def set_name(self,name):
        self.__name=name
            
    def set_pin_hash(self,pin):
        self.__pin=__hash_pin(pin)
        
    def set_balance(self,balance):
        self.__balance=balance
        
        
    # UTILITY
    def deposit(self,amount):
        if amount<=0:
            return False
        
        self.__balance +=amount
        return True
    
    
    def withdraw(self,amount):
        if amount<=0 or amount>self.__balance:
            return False
            
        self.__balance -= amount
        return True
        
        
        
    #DataBase CRUD
    @classmethod
    def load_from_db(cls,account_number,pin):
        connection=connect_to_database()
        if not connection:
            return False
        try:
            cursor=connection.cursor()
            cursor.execute(
                "SELECT account_number,name,pin,balance FROM accounts WHERE account_number=%s",
                (account_number,),
            )
            result=cursor.fetchone()
            connection.commit()
            cursor.close()
            if result:
                stored_pin_hash=result[2]
                if __verify_pin(pin,stored_pin_hash):
                    account=cls(result[1],"",result[0])
                    account.set_balance(float(result[3]))
                    return account
                    
        except Exception as error:
            print(f"Error loading account, {error}")
            return None
        
         
    def save_to_db(self):
        connection=connect_to_database()
        if not connection:
            return False
        try:
            cursor=connection.cursor()
            cursor.execute(
                """
                INSERT INTO accounts (account_number,name,pin,balance)
                values(%s,%s,%s,%s)
                ON CONFLICT (account_number)
                DO UPDATE SET name=%s,pin=%s,balance=%s
                    (
                        self.__account_number,
                        self.__name,
                        self.__pin,
                        self.__balance,
                        self.__name,
                        self.__pin,
                        self.__balance,
                    ),
                """  
            )
            # result=cursor.fetchone()
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error creating/updating account, {error}")
            return None
        
    
    def delect_from_db(self):
        connection=connect_to_database()
        if not connection:
            return False
        try:
            cursor=connection.cursor()
            cursor.execute(
                "DELETE FROM accounts WHERE account_number=%s",
                (self.account_number,),
            )
            # result=cursor.fetchone()
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error cloasing account, {error}")
            return None
        
    
# AUDIT CLASS
class Audit:
    @staticmethod
    def log_action(account_number,holder_name,action,amount=0.0):
        connection=connect_to_database()
        if not connection:
            return False
        
        try:
            cursor=connection.cursor()
            cursor.execute(
                "INSERT INTO audit (account_number,holder_name,action,amount) VALUES (%s,%s,%s,%s)",
                (
                    account_number,
                    holder_name,
                    action,
                    amount,
                ),
            )
            # result=cursor.fetchone()
            connection.commit()
            cursor.close()  
            return True
        except Exception as error:
            print(f"Error auditing actions, {error}")
            return None
            
    @staticmethod
    def get_single_audit_log(account_number):
        connection=connect_to_database()
        if not connection:
            return []
        
        try:
            cursor=connection.cursor()
            cursor.execute(
               """
                SELECT id,holder_name,action,amount,Timestamp
                FROM audit
                WHERE account_number=%s
                ORDER BY timestamp DESC
               """,
                (account_number)
            )
            results=cursor.fetchone()
            connection.commit()
            cursor.close()
            logs=[]
            for row in results:
                logs.append({
                    "id":row[0],
                    "holder_name":row[1],
                    "action":row[2],
                    "amount":row[3],
                    "timestamp":row[4],
                    
                })
            return logs
        except Exception as error:
            print(f"Error loging {account_number} actions, {error}")
            return None
            
    @staticmethod
    def get_all_audit_log():
        connection=connect_to_database()
        if not connection:
            return []
        
        try:
            cursor=connection.cursor()
            cursor.execute(
               """
                SELECT id,holder_name,action,amount,Timestamp
                FROM audit
                ORDER BY timestamp DESC
               """
            )
            results=cursor.fetchone()
            connection.commit()
            cursor.close()
            logs=[]
            for row in results:
                logs.append({
                    "id":row[0],
                    "holder_name":row[1],
                    "action":row[2],
                    "amount":row[3],
                    "timestamp":row[4],
                    
                })
            return logs
        except Exception as error:
            print(f"Error loging all audit actions, {error}")
            return None
    
    @staticmethod
    def clear_single_audit_log(account_number):
        connection=connect_to_database()
        if not connection:
            return False
        
        try:
            cursor=connection.cursor()
            cursor.execute("DELETE FROM audit WHERE account_number=%s",
                           (account_number,),
            )
            connection.commit()
            cursor.close()
            
            return True
        except Exception as error:
            print(f"Error clearing {account_number} actions, {error}")
            return False
            
    @staticmethod
    def clear_all_audit_log():
        connection=connect_to_database()
        if not connection:
            return False
        
        try:
            cursor=connection.cursor()
            cursor.execute("DELETE FROM audit")
            
            connection.commit()
            cursor.close()
            return True
        except Exception as error:
            print(f"Error clearing all audit actions, {error}")
            return None
                
    
    # BANKSYYSTEM CLASS 
    class BankSystem:
        def __init__(self):
            inialize_tables()
    
        def create_account(self,name,pin):
            account=Account(name,pin)
            if account.save_to_db():
                Audit.log_action(
                    account.get_account_number(),account.get_name(),"Account Create",0.0
                )
                return account
            return None
            
        def read_account(self,account_number,pin):
            account=Account.load_from_db(account_number,pin)
            if account:
                Audit.log_action(account_number,account.get_name(),"Details checked",0.0)
                return account
            return None
        def read_account(self,account):
            return account.save_to_db()    
        
        def delete_account(self,account_number,pin):
            account=Account.load_from_db(account_number,pin)
            if account:
                success=account.delete_from_db()
                if success:
                    Audit.log_action(account_number,account.get_name(),"Account closed",0.0)
                    return True
            return False      
        
        def deposite(self,account_number,pin,amount):
            account=Account.load_from_db(account_number,pin)
            if account and account.deposit(amount):
                Audit.log_action(
                    account_number,account.get_name(),"Amount Deposited",amount
                )
                return True
            return False      
        
        def withdraw(self,account_number,pin,amount):
            account=Account.load_from_db(account_number,pin)
            if account and account.withdraw(amount):
                Audit.log_action(
                    account_number,account.get_name(),"Amount Deposited",amount
                )
                return True
            return False   
        
        def get_account_balance(self,account_number,pin):
            account=Account.load_from_db(account_number,pin)
            if account:
                Audit.log_action(
                    account_number,account.get_name(),"Balance Checked",0.0
                )
                return account.get_balance
            return None       