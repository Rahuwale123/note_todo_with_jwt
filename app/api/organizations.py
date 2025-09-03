from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user, require_admin_role
from app.models.organization import Organization
from app.models.user import User, UserRole
from app.schemas.organization import OrganizationResponse, OrganizationWithUsers
from typing import List, Optional

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


@router.get("/public", response_model=List[dict])
def get_public_organizations(db: Session = Depends(get_db)):
    organizations = db.query(Organization).all()
    return [
        {
            "id": org.id,
            "name": org.name,
            "created_at": org.created_at
        }
        for org in organizations
    ]


@router.get("/search", response_model=List[dict])
def search_organizations(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    organizations = db.query(Organization).filter(Organization.name.ilike(f"%{q}%")).all()
    return [
        {
            "id": org.id,
            "name": org.name,
            "created_at": org.created_at
        }
        for org in organizations
    ]


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


@router.put("/{organization_id}/users/{user_id}")
def update_user_role(
    organization_id: int,
    user_id: int,
    role: UserRole,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    if current_user.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access your organization's data."
        )
    
    user = db.query(User).filter(
        User.id == user_id,
        User.organization_id == organization_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in this organization"
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    user.role = role
    db.commit()
    
    return {"message": f"User {user.username} role updated to {role.value}"}


@router.delete("/{organization_id}/users/{user_id}")
def remove_user_from_organization(
    organization_id: int,
    user_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    if current_user.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. You can only access your organization's data."
        )
    
    user = db.query(User).filter(
        User.id == user_id,
        User.organization_id == organization_id
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found in this organization"
        )
    
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove yourself from the organization"
        )
    
    db.delete(user)
    db.commit()
    
    return {"message": f"User {user.username} removed from organization"}
