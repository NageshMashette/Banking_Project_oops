from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = FastAPI()

class Banking:
    """
    A class to represent a bank account.
    """

    def __init__(self, person_name, balance=0):
        """
        Initialize the bank account with a person's name and an optional balance.
        """
        self.person_name = person_name
        self.balance = balance
        logging.info(f"Banking account created for {self.person_name} with initial balance {self.balance}")
        
    def deposit(self, amount):
        """
        Deposit a specified amount into the account.
        """
        if amount <= 0:
            logging.warning(f"Attempt to deposit non-positive amount {amount} to {self.person_name}'s account")
            raise HTTPException(status_code=400, detail="Deposit amount must be positive")
        self.balance += amount
        logging.info(f"Deposited {amount} to {self.person_name}'s account. New balance: {self.balance}")
        return f"Amount {amount} is deposited in {self.person_name} account"
        
    def withdraw(self, amount):
        """
        Withdraw a specified amount from the account if sufficient balance is available.
        """
        if amount <= 0:
            logging.warning(f"Attempt to withdraw non-positive amount {amount} from {self.person_name}'s account")
            raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")
        if amount > self.balance:
            logging.warning(f"Attempt to withdraw {amount} from {self.person_name}'s account failed due to insufficient balance")
            raise HTTPException(status_code=400, detail="Insufficient balance")
        else:
            self.balance -= amount
            logging.info(f"Withdrew {amount} from {self.person_name}'s account. New balance: {self.balance}")
            return f"Amount {amount} is withdrawn from {self.person_name} account"
            
    def check_balance(self):
        """
        Check the current balance of the account.
        """
        logging.info(f"Checked balance for {self.person_name}. Current balance: {self.balance}")
        return f"Balance in {self.person_name} account is {self.balance}"

account = Banking("John")

class Transaction(BaseModel):
    amount: float

@app.post("/deposit")
def deposit(transaction: Transaction):
    try:
        return account.deposit(transaction.amount)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Unexpected error during deposit: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/withdraw")
def withdraw(transaction: Transaction):
    try:
        return account.withdraw(transaction.amount)
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Unexpected error during withdrawal: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/check_balance")
def check_balance():
    try:
        return account.check_balance()
    except Exception as e:
        logging.error(f"Unexpected error during balance check: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
