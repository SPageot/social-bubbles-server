from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from model.user import RegisteredUserType

ph = PasswordHasher()

def password_hasher(password: str) -> str:
    return ph.hash(password)

def password_verify(user_password, registered_password):
    try:
        ph.verify(registered_password, user_password)
        return True
    except Exception as e:
        return False
    

    
key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt_data(data: str) -> str:
    return cipher_suite.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(encrypted_data: str) -> str:
    return cipher_suite.decrypt(encrypted_data.encode('utf-8')).decode('utf-8')


def filter_user(user:RegisteredUserType):
    return {
        "_id":user["_id"],
        "username":user["username"],
        "firstName":user["firstName"],
        "lastName":user["lastName"],
        "email":user["email"],
        "phoneNumber":user["phoneNumber"]
    }