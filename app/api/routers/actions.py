from fastapi import APIRouter, status, Response, Request
from fastapi.param_functions import Header

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app import utils

from app.api.routers.users import users
from app.api.routers.products import products

import math

router = APIRouter()

class Deposit(BaseModel):
    coinValue: int

class BuyRequest(BaseModel):
    productId: str
    amount: int
    
deposits = {}

# Format of the deposits dictionary:
# { 
#   'user1': {10: 3, 5: 2}, 
#   'user3': {50: 2}
# }

valid_coin_values = [5, 10, 20, 50, 100]

@router.post("/$deposit/")
async def depositCoin(deposit: Deposit, request: Request):
    deposit = deposit.model_dump()
    
    coin_value = deposit["coinValue"]
    if (coin_value not in valid_coin_values):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})
    
    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)

    if (username not in users.keys()):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})
    
    if (users[username]["role"] != "BUYER"):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={})
    
    if (username in deposits):
        if (coin_value in deposits[username]):
            deposits[username][coin_value] += 1
        else:
            deposits[username][coin_value] = 1
    else:
        deposits[username] = {}
        deposits[username][coin_value] = 1

    print(deposits)
    
    response = {"balance": []}
    for coin in deposits[username]:
        current = {}
        current["coinValue"] = coin
        current["amount"] = deposits[username][coin]
        response["balance"].append(current);

    return response

@router.post("/$buy/")
async def buyProduct(buyRequest: BuyRequest, request: Request):
    buyRequest = buyRequest.model_dump()
    
    productId = buyRequest["productId"]
    amount = buyRequest["amount"]

    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)

    if (username not in users.keys()):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})

    if (users[username]["role"] != "BUYER"):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={})

    if (productId not in products):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})

    total_product_price = products[productId]["price"] * amount
    print (total_product_price)

    total_balance = 0
    if (username in deposits):
        for coin in deposits[username]:
            total_balance += coin * deposits[username][coin]

    print (total_balance)

    if (total_balance < total_product_price):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={})
    
    balance = total_balance - total_product_price

    change = []
    while (balance >= 5):
        if (balance >= 100):            
            change.append({"coinValue": 100, "amount": math.floor(balance / 100)})
            balance = balance % 100
        elif (balance >= 50):            
            change.append({"coinValue": 50, "amount": math.floor(balance / 50)})
            balance = balance % 50
        elif (balance >= 20):
            change.append({"coinValue": 20, "amount": math.floor(balance / 20)})
            balance = balance % 20
        elif (balance >= 10):
            change.append({"coinValue": 10, "amount": math.floor(balance / 10)})
            balance = balance % 10
        elif (balance >= 5):
            change.append({"coinValue": 5, "amount": math.floor(balance / 5)})
            balance = balance % 5

    deposits.pop(username)

    response = {}

    response["total_spent"] = total_product_price
    response["amount"] = amount
    response["product"] = products[productId]  
    response["change"] = change

    return response

@router.post("/$reset/")
async def reset(request: Request):
    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)

    if (username not in users.keys()):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})

    if (users[username]["role"] != "BUYER"):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={})

    if (username in deposits):
        deposits.pop(username)