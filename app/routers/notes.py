"""
Routes for managing notes.

Features:
1. Create a note
2. Get all notes of the current user
3. Get a single note
4. Update a note
5. Delete a note

Authentication is required for all endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix="/api/v1/notes",tags=["Notes"],)


# ==========================================================
# Create Note
# ==========================================================

@router.post("/",response_model=schemas.NoteResponse,status_code=status.HTTP_201_CREATED,)

def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Create a new note for the authenticated user.
    """

    new_note = models.Note(
        title=note.title,
        body=note.body,
        category_id=note.category_id,
        owner_id=current_user.id,
    )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


# ==========================================================
# Get All Notes
# ==========================================================

@router.get("/",response_model=list[schemas.NoteResponse],)

def get_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return all notes that belong to the authenticated user.
    """

    notes = (
        db.query(models.Note)
        .filter(models.Note.owner_id == current_user.id)
        .all()
    )

    return notes


# ==========================================================
# Get Single Note
# ==========================================================

@router.get("/{id}",response_model=schemas.NoteResponse,)

def get_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return a single note.

    If the note does not belong to the current user,
    return 404
    """

    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == id,
            models.Note.owner_id == current_user.id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

    return note


# ==========================================================
# Update Note
# ==========================================================

@router.put("/{id}",response_model=schemas.NoteResponse,)

def update_note(
    id: int,
    updated_note: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Update a note that belongs to the current user.
    """

    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == id,
            models.Note.owner_id == current_user.id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

    note.title = updated_note.title
    note.body = updated_note.body
    note.category_id = updated_note.category_id

    db.commit()
    db.refresh(note)

    return note


# ==========================================================
# Delete Note
# ==========================================================

@router.delete( "/{id}", status_code=status.HTTP_204_NO_CONTENT,)

def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Delete a note that belongs to the current user.
    """

    note = (
        db.query(models.Note)
        .filter(
            models.Note.id == id,
            models.Note.owner_id == current_user.id,
        )
        .first()
    )

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )

    db.delete(note)
    db.commit()

    return