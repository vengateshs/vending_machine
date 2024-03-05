from fastapi import APIRouter, status, Response, Request
from fastapi.param_functions import Header

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

router = APIRouter()

class User(BaseModel):
    userName: str
    firstName: str
    lastName: str
    email: str
    role: str

class UserUpdate(BaseModel):
    firstName: str = None 
    lastName: str = None

users = {}

# Format of the users dictionary:
# dict_keys(['u1', 'u2'])
# dict_values([
#   {'userName': 'u1', 'firstName': 'aaa', 'lastName': 'bbb', 'email': 'aaa@aaa.com', 'role': 'SELLER'}, 
#   {'userName': 'u2', 'firstName': 'aaa', 'lastName': 'bbb', 'email': 'aaa@aaa.com', 'role': 'SELLER'}
#   ])

@router.post("/users/")
async def createUser(user: User):
    new_user = user.model_dump()
    user_name = new_user["userName"]
    if (user_name in users.keys()):
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={})
    else:
        users[user_name] = new_user

    print(users.keys())
    print(users.values())

    return new_user

@router.get("/users/")
async def getAllUsers(offset: int = 0,
                      limit: int = 100):
    response_dict = {}

    response_dict["offset"] = offset
    response_dict["limit"] = limit
    response_dict["total"] = len(users)
    response_dict["items"] = list(users.values())

    return response_dict

@router.get("/users/{userName}")
async def getUser(userName: str):
    if (not userName in users.keys()):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    else:
        return users[userName]

@router.delete("/users/{userName}")
async def deleteUser(userName: str):
    if (not userName in users.keys()):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    else:
        return users.pop(userName)
    
@router.patch("/users/{userName}")
async def patchUser(userName: str, user: UserUpdate):
    if (not userName in users.keys()):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={})
    else:
        user_update = user.model_dump()
        if (user_update["firstName"] is not None):
            users[userName]["firstName"] = user_update["firstName"]
        if (user_update["lastName"] is not None):
            users[userName]["lastName"] = user_update["lastName"]
        return users[userName]
