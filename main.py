from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.responses import JSONResponse


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
        
    def deposit(self, amount):
        """
        Deposit a specified amount into the account.
        """
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Deposit amount must be positive")
        self.balance += amount
        return f"Amount {amount} is deposited in {self.person_name} account"
        
    def withdraw(self, amount):
        """
        Withdraw a specified amount from the account if sufficient balance is available.
        """
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Withdrawal amount must be positive")
        if amount > self.balance:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        else:
            self.balance -= amount
            return f"Amount {amount} is withdrawn from {self.person_name} account"
            
    def check_balance(self):
        """
        Check the current balance of the account.
        """
        return f"Balance in {self.person_name} account is {self.balance}"

account = Banking("John")

class Transaction(BaseModel):
    amount: float

@app.post("/deposit")
def deposit(transaction: Transaction):
    try:
        message = account.deposit(transaction.amount)
        return JSONResponse(content={"message": message})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/withdraw")
def withdraw(transaction: Transaction):
    try:
        message = account.withdraw(transaction.amount)
        return JSONResponse(content={"message": message})
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/check_balance")
def check_balance():
    try:
        balance = account.check_balance()
        return JSONResponse(content={"balance": balance})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
