from fastapi import FastAPI, Request 
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/user/create")
@limiter.limit("5/minute")
async def create_user(request:Request):
    user = await request.json()
    return user

@app.get("/user/{user_id}")
@limiter.limit("5/minute")
async def get_user(request: Request):
    get_user_id_params = request.path_params
    user_id = get_user_id_params["user_id"]
  