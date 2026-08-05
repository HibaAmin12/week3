"""
Routes for managing notes.

Features:
1. Create a note
2. Get all notes of current user
3. Get single note
4. Update note
5. Delete note

Authentication is required for all endpoints.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db
from app.oauth2 import get_current_user


router = APIRouter(
    prefix="/api/v1/notes",
    tags=["Notes"]
)


# ==========================================================
# Create Note
# ==========================================================

@router.post(
    "/",
    response_model=schemas.NoteResponse,
    status_code=status.HTTP_201_CREATED
)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    # Validate category only if category_id exists
    if note.category_id and note.category_id > 0:

        category = (
            db.query(models.Category)
            .filter(
                models.Category.id == note.category_id
            )
            .first()
        )

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )


    new_note = models.Note(
        title=note.title,
        body=note.body,
        owner_id=current_user.id,
        category_id=None if note.category_id == 0 else note.category_id
    )


    db.add(new_note)
    db.commit()
    db.refresh(new_note)


    return new_note



# ==========================================================
# Get All Notes
# ==========================================================

@router.get(
    "/",
    response_model=list[schemas.NoteResponse]
)
def get_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    notes = (
        db.query(models.Note)
        .filter(
            models.Note.owner_id == current_user.id
        )
        .all()
    )

    return notes



# ==========================================================
# Get Single Note
# ==========================================================

@router.get(
    "/{id}",
    response_model=schemas.NoteResponse
)
def get_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == id,
            models.Note.owner_id == current_user.id
        )
        .first()
    )


    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )


    return note



# ==========================================================
# Update Note
# ==========================================================

@router.put(
    "/{id}",
    response_model=schemas.NoteResponse
)
def update_note(
    id: int,
    updated_note: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == id,
            models.Note.owner_id == current_user.id
        )
        .first()
    )


    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )


    # Validate category if category is changed
    if updated_note.category_id and updated_note.category_id > 0:

        category = (
            db.query(models.Category)
            .filter(
                models.Category.id == updated_note.category_id
            )
            .first()
        )

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )


    if updated_note.title is not None:
        note.title = updated_note.title


    if updated_note.body is not None:
        note.body = updated_note.body


    if updated_note.category_id is not None:
        note.category_id = (
            None if updated_note.category_id == 0
            else updated_note.category_id
        )


    # Update modification time
    note.updated_at = datetime.utcnow()


    db.commit()
    db.refresh(note)


    return note



# ==========================================================
# Delete Note
# ==========================================================

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == id,
            models.Note.owner_id == current_user.id
        )
        .first()
    )


    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )


    db.delete(note)
    db.commit()


    return None