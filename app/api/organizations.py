from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user, require_admin_role
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationResponse, OrganizationWithUsers
from typing import List

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/me", response_model=OrganizationResponse)
def get_my_organization(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    return organization


@router.get("/{organization_id}/users", response_model=List[dict])
def get_organization_users(
    organization_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    if current_user.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access your organization's data."
        )
    
    users = db.query(User).filter(User.organization_id == organization_id).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": user.role.value,
            "created_at": user.created_at
        }
        for user in users
    ]
