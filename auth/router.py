from auth.jwt_utils import create_access_token
from auth.middelware import get_current_user
from auth.schemas import UserCreate, UserLogin, UserResponse
from auth.utils import get_password_hash
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from database.dependencies import get_db
from .services import UserAuth
auth_router = APIRouter()

@auth_router.post("/signup/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserAuth.create_user_service(user, db)
    return db_user

@auth_router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    access_token = UserAuth.authenticate_user_service(user.email, user.password, db)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/logout/")
def logout():
    return {"message": "Logout successful"}

@auth_router.get("/check-auth/")
def check_auth(current_user: User = Depends(get_current_user)):
    return UserAuth.check_user_authentication_service(current_user)