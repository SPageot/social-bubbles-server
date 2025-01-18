from pydantic import BaseModel


class UserLoginType(BaseModel):
    username: str
    password: str

class UserRegisterType(BaseModel):
    username: str
    password: str
    firstName: str
    lastName: str
    phoneNumber: str
    email:str

class RegisteredUserType(UserRegisterType):
    _id:str