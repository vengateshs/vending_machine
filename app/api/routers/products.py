from fastapi import APIRouter, status, Response, Request
from fastapi.param_functions import Header
from app import utils

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

import uuid

from app.api.routers.users import users

router = APIRouter()

class Product(BaseModel):
    name: str
    price: float

products = {}

# Format of the products dictionary:
#dict_keys(['a6d52530-2556-41f4-b4f9-67f63f1a7f04', '88198168-c06d-4a0e-9ca8-e44fa157206e'])
#dict_values([
#   {'name': 'p1', 'price': 1.5, 'id': 'a6d52530-2556-41f4-b4f9-67f63f1a7f04', 'createdBy': 'user1'},  
#   {'name': 'p1', 'price': 1.5, 'id': '88198168-c06d-4a0e-9ca8-e44fa157206e', 'createdBy': 'user2'}])

@router.post("/products/")
async def createProduct(product: Product, request: Request):
    new_product = product.model_dump()
    
    new_id = str(uuid.uuid4())
    new_product["id"] = new_id

    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)

    if (username not in users.keys()):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})

    if (users[username]["role"] != "SELLER"):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={})
        
    new_product["createdBy"] = username

    products[new_id] = new_product

    print(products.keys())
    print(products.values())

    return new_product

@router.get("/products/")
async def getAllProducts(offset: int = 0,
                      limit: int = 100):
    response_dict = {}

    response_dict["offset"] = offset
    response_dict["limit"] = limit
    response_dict["total"] = len(products)
    products_list = list(products.values())
    response_dict["items"] = products_list[offset: offset + limit]

    return response_dict

@router.get("/products/{productId}")
async def getProduct(productId: str):
    if (not productId in products.keys()):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    else:
        return products[productId]

@router.delete("/products/{productId}")
async def deleteProduct(productId: str, request: Request):
    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)

    if (username not in users.keys()):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})
        
    if (not productId in products.keys()):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)
    
    if (products[productId]["createdBy"] != username):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={})
    else:
        return products.pop(productId)
    
@router.patch("/products/{productId}")
async def patchProduct(productId: str, product: Product, request: Request):
    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)

    if (username not in users.keys()):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={})
        
    if (not productId in products.keys()):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})

    auth_token = request.headers.get("Authorization")
    auth_scheme, username, password = utils.decodeAuthToken(auth_token)
    
    if (products[productId]["createdBy"] != username):
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={})
    else:
        product = product.model_dump()
        if (product["name"] is not None):
            products[productId]["name"] = product["name"]
        if (product["price"] is not None):
            products[productId]["price"] = product["price"]            
        return products[productId]
