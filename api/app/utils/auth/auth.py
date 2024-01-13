from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv


load_dotenv()

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"])


# This function is used to hash the password.
def hashPassword(plain_password):
    return pwd_context.hash(plain_password)

# This function is used to verify the password.
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# This function is used to create a new access token and return it.
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.time.
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except JWTError:
        return None

