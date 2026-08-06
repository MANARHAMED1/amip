import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from api.database import fetch_one

router = APIRouter()

JWT_SECRET = os.getenv("AMIP_JWT_SECRET", "amip-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

security = HTTPBearer()


class LoginRequest(BaseModel):
    username: str
    password: str


def create_token(user_id: int, username: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/login")
def login(req: LoginRequest):
    user = fetch_one(
        "SELECT user_id, username, password_hash, full_name, role, active "
        "FROM amip_user WHERE username = %s",
        (req.username,),
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.get("active", True):
        raise HTTPException(status_code=403, detail="Account disabled")

    if not bcrypt.checkpw(req.password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user["user_id"], user["username"], user["role"])

    return {
        "token": token,
        "user": {
            "user_id": user["user_id"],
            "username": user["username"],
            "full_name": user["full_name"],
            "role": user["role"],
        },
    }


@router.get("/me")
def get_current_user(user=Depends(verify_token)):
    u = fetch_one(
        "SELECT user_id, username, full_name, role FROM amip_user WHERE user_id = %s",
        (user["user_id"],),
    )
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u
