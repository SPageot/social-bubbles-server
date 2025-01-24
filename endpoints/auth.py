from fastapi import APIRouter, Request, HTTPException
from security.limiter import limiter
from security.functions import password_hasher, password_verify, encrypt_data,decrypt_data,filter_user
from pymongo import MongoClient
from model.user import UserLoginType, UserRegisterType, RegisteredUserType
import os

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
client = MongoClient(MONGO_DB_URI)
db = client['SocialBubbles']
collection = db['users']

router = APIRouter()

@router.post("/register")
@limiter.limit("5/minute")
async def create_user(request:Request):
    user: UserRegisterType = await request.json()
    user["username"] = user["username"].lower()
    check_user_is_registered = collection.find_one({"username":user["username"] ,"phoneNumber": user["phoneNumber"]})
    if check_user_is_registered is None:
            user["username"] = user["username"].lower()
            user["email"] = encrypt_data(user["email"])
            user["phoneNumber"]= encrypt_data(user["phoneNumber"])
            user["password"] = password_hasher(user["password"])
            collection.insert_one(user)
            return "User is Successfully Registered!!"
    else:
         raise HTTPException(status_code=409, detail="User is already registered")


@router.post("/login")
@limiter.limit("5/minute")
async def login_user(request: Request):
    user:UserLoginType = await request.json()
    user["username"] = user["username"].lower()
    registered_user: RegisteredUserType = collection.find_one({"username": user["username"]})
    if registered_user is None:
         raise HTTPException(status_code=404,detail="User is not registered")
    else:
        if password_verify(user["password"], registered_user["password"]):
            registered_user["_id"] = str(registered_user["_id"])
            registered_user["email"] = decrypt_data(registered_user["email"])
            registered_user["phoneNumber"] = decrypt_data(registered_user["phoneNumber"])
            user_details_filtered = filter_user(registered_user)
            return user_details_filtered
        else:
             raise HTTPException(status_code=401, detail="Password is incorrect")