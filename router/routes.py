from fastapi import APIRouter, Request
from security.limiter import limiter

router = APIRouter()

@router.post("/user/create")
@limiter.limit("5/minute")
async def create_user(request:Request):
    user = await request.json()
    return user

@router.post("/login")
@limiter.limit("5/minute")
async def login_user(request: Request):
    user_login_details = await request.json()
    return user_login_details