from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.deps import get_current_user, require_admin_role
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse, TodoWithUser
from typing import List

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/", response_model=List[TodoWithUser])
def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todos = db.query(Todo).filter(Todo.organization_id == current_user.organization_id).all()
    
    result = []
    for todo in todos:
        todo_dict = {
            "id": todo.id,
            "title": todo.title,
            "completed": todo.completed,
            "organization_id": todo.organization_id,
            "created_by": todo.created_by,
            "created_at": todo.created_at,
            "updated_at": todo.updated_at,
            "created_by_username": todo.created_by_user.username
        }
        result.append(todo_dict)
    
    return result


@router.post("/", response_model=TodoResponse)
def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = Todo(
        title=todo_data.title,
        completed=todo_data.completed,
        organization_id=current_user.organization_id,
        created_by=current_user.id
    )
    
    db.add(todo)
    db.commit()
    db.refresh(todo)
    
    return todo


@router.get("/{todo_id}", response_model=TodoWithUser)
def get_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.organization_id == current_user.organization_id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    return {
        "id": todo.id,
        "title": todo.title,
        "completed": todo.completed,
        "organization_id": todo.organization_id,
        "created_by": todo.created_by,
        "created_at": todo.created_at,
        "updated_at": todo.updated_at,
        "created_by_username": todo.created_by_user.username
    }


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.organization_id == current_user.organization_id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    if todo_data.title is not None:
        todo.title = todo_data.title
    if todo_data.completed is not None:
        todo.completed = todo_data.completed
    
    db.commit()
    db.refresh(todo)
    
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    current_user: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.organization_id == current_user.organization_id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    
    db.delete(todo)
    db.commit()
    
    return {"message": "Todo deleted successfully"}
