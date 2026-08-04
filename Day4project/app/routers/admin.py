"""
Admin routes.

These routes are accessible only to users
with the admin role.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.dependencies import get_db
from app.oauth2 import get_current_user

router = APIRouter( prefix="/api/v1/admin", tags=["Admin"],)


@router.get("/notes",response_model=list[schemas.NoteResponse],status_code=status.HTTP_200_OK,)

def get_all_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Return all notes from all users.

    Only administrators are allowed to access this endpoint.
    """

    # Check if the current user is an admin.
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required.",
        )

    notes = db.query(models.Note).all()

    return notes