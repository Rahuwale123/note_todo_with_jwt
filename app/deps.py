from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import verify_token
from app.models.user import User, UserRole
from app.schemas.user import TokenData

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        token_data = TokenData(**payload)
        if token_data.user_id is None:
            raise credentials_exception
            
    except Exception:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    
    return user


def get_current_user_token_data(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        token_data = TokenData(**payload)
        if token_data.user_id is None:
            raise credentials_exception
            
    except Exception:
        raise credentials_exception
    
    return token_data


def require_admin_role(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. ADMIN role required."
        )
    return current_user


def require_same_organization(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    def _check_org_access(organization_id: int):
        if current_user.organization_id != organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. You can only access your organization's data."
            )
        return organization_id
    
    return _check_org_access
