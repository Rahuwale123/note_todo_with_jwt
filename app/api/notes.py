from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user, require_admin_role
from app.models.note import Note
from app.models.user import User
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse, NoteWithUser
from typing import List

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=List[NoteWithUser])
@router.get("/", response_model=List[NoteWithUser])
def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notes = db.query(Note).filter(Note.organization_id == current_user.organization_id).all()
    
    result = []
    for note in notes:
        note_dict = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "organization_id": note.organization_id,
            "created_by": note.created_by,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
            "created_by_username": note.created_by_user.username
        }
        result.append(note_dict)
    
    return result


@router.get("/my-notes", response_model=List[NoteWithUser])
def get_my_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    notes = db.query(Note).filter(
        Note.organization_id == current_user.organization_id,
        Note.created_by == current_user.id
    ).all()
    
    result = []
    for note in notes:
        note_dict = {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "organization_id": note.organization_id,
            "created_by": note.created_by,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
            "created_by_username": note.created_by_user.username
        }
        result.append(note_dict)
    
    return result


@router.post("", response_model=NoteResponse)
@router.post("/", response_model=NoteResponse)
def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = Note(
        title=note_data.title,
        content=note_data.content,
        organization_id=current_user.organization_id,
        created_by=current_user.id
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return note


@router.get("/{note_id}", response_model=NoteWithUser)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.organization_id == current_user.organization_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "organization_id": note.organization_id,
        "created_by": note.created_by,
        "created_at": note.created_at,
        "updated_at": note.updated_at,
        "created_by_username": note.created_by_user.username
    }


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note_data: NoteUpdate,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.organization_id == current_user.organization_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    if note_data.title is not None:
        note.title = note_data.title
    if note_data.content is not None:
        note.content = note_data.content
    
    db.commit()
    db.refresh(note)
    
    return note


@router.delete("/{note_id}")
def delete_note(
    note_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    note = db.query(Note).filter(
        Note.id == note_id,
        Note.organization_id == current_user.organization_id
    ).first()
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    
    db.delete(note)
    db.commit()
    
    return {"message": "Note deleted successfully"}
