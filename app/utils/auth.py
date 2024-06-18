import binascii
import hashlib
import os
import secrets
import time

from fastapi import Header, HTTPException
from fastapi.param_functions import Depends
from pymongo.database import Database

from app.models.database import get_db


def generate_api_key(username: str) -> str:
    """
    Generate the API key for the user with its username
    """
    timestamp = str(time.time()).encode("utf-8")
    unique_id = secrets.token_urlsafe(8).encode("utf-8")
    seed = username.encode("utf-8") + os.urandom(16) + timestamp + unique_id
    hashed_seed = hashlib.sha512(seed).hexdigest()
    return hashed_seed[: len(hashed_seed) // 2]


def check_api_key(
    username: str, api_key: str = Header(...), db: Database = Depends(get_db)
) -> bool:
    """
    Check if the API key exists in the database
    """
    user = db.users.find_one({"username": username})
    if not user or user["api_key"] != api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_bytes = password.encode("utf-8")
    hashed_password = hashlib.pbkdf2_hmac("sha256", password_bytes, salt, 100000)
    return binascii.hexlify(salt + hashed_password).decode("ascii")


"""
def verify_password(password: str, hashed_password: str) -> bool:
  stored_password = binascii.unhexlify(hashed_password)
  salt = stored_password[:16]
  hashed_password = stored_password[16:]
  password_bytes = password.encode("utf-8")
  new_hash = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, 100000)
  return new_hash == hashed_password
"""
