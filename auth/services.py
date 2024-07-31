# auth/services.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .models import User
from .schemas import UserCreate
from .utils import get_password_hash, verify_password
from .jwt_utils import create_access_token

class UserAuth:

  def create_user_service(user: UserCreate, db: Session) -> User:
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

  def authenticate_user_service(email: str, password: str, db: Session) -> str:
      user = db.query(User).filter(User.email == email).first()
      if not user or not user.verify_password(password):
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
      access_token = create_access_token(data={"sub": user.email})
      return access_token

  def check_user_authentication_service(current_user: User) -> dict:
      return {"status": "authenticated", "user": current_user.email}
