from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from datetime import timedelta
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if user_data.organization_id:
        organization = db.query(Organization).filter(Organization.id == user_data.organization_id).first()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
        role = UserRole.MEMBER
        organization_id = user_data.organization_id
    else:
        organization = Organization(name=f"Organization for {user_data.username}")
        db.add(organization)
        db.flush()
        role = UserRole.ADMIN
        organization_id = organization.id
    
    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        password_hash=hashed_password,
        role=role,
        organization_id=organization_id
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "user_id": user.id,
            "organization_id": user.organization_id,
            "role": user.role.value
        },
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
