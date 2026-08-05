# """
# Category Router

# This module provides API endpoints for managing categories.

# Relationship:

# Category (1) -------- (*) Note

# One category can have many notes.

# Endpoints:

# POST /api/v1/categories/
#     Create category

# GET /api/v1/categories/
#     Get all categories
# """


# from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session

# from app import models, schemas
# from app.dependencies import get_db


# # ==========================================================
# # Router Configuration
# # ==========================================================

# router = APIRouter(
#     prefix="/api/v1/categories",
#     tags=["Categories"]
# )



# # ==========================================================
# # Create Category
# # ==========================================================

# @router.post(
#     "/",
#     response_model=schemas.CategoryResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_category(
#     category: schemas.CategoryCreate,
#     db: Session = Depends(get_db)
# ):
#     """
#     Create a new category.

#     Example body:

#     {
#         "name": "Programming"
#     }
#     """


#     # Check duplicate category
#     existing_category = (
#         db.query(models.Category)
#         .filter(
#             models.Category.name == category.name
#         )
#         .first()
#     )


#     if existing_category:
#         raise HTTPException(
#             status_code=400,
#             detail="Category already exists."
#         )


#     # Create SQLAlchemy object
#     new_category = models.Category(
#         name=category.name
#     )


#     # Add to session
#     db.add(new_category)


#     # Save permanently
#     db.commit()


#     # Refresh to get generated id
#     db.refresh(new_category)


#     return new_category





# # ==========================================================
# # Get All Categories
# # ==========================================================

# @router.get(
#     "/",
#     response_model=list[schemas.CategoryResponse]
# )
# def get_categories(
#     db: Session = Depends(get_db)
# ):
#     """
#     Return all categories.
#     """


#     categories = (
#         db.query(models.Category)
#         .all()
#     )


#     return categories