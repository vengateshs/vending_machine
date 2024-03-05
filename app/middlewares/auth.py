from fastapi import Request, status
from fastapi.responses import JSONResponse
from app import utils

allowed_users = { "user1": "pwd1",  
                  "user2": "pwd2",
                  "user3": "pwd3",
                  "user4": "pwd4",
                  "user5": "pwd5",
                  "user6": "pwd6",
                  "user7": "pwd7",
                  "user8": "pwd8",
                  "user9": "pwd9",
                  "user10": "pwd10"
                }

async def auth_middleware(
    request: Request,
    call_next,
):
    unprotected_apis = [{"method":"POST", "api":"users"}, 
                        {"method":"GET", "api":"products"}]

    bProtectedAPI = True

    method = request.method
    api = request.url.path.split('/')[1]

    current_api = {"method":method, "api":api}

    if (current_api in unprotected_apis):
        bProtectedAPI = False

    if (bProtectedAPI):
        auth_token = request.headers.get("Authorization")
        print(auth_token)
        if auth_token is None:
            return JSONResponse(None, status.HTTP_401_UNAUTHORIZED, {"WWW-Authenticate": "Basic"})
        else:
            auth_scheme, username, password = utils.decodeAuthToken(auth_token)
            if (auth_scheme != 'Basic' or 
                username not in allowed_users or
                password != allowed_users[username]): 
                return JSONResponse(None, status.HTTP_401_UNAUTHORIZED, {"WWW-Authenticate": "Basic"})              
    
    return await call_next(request)