from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, nullable=False, default=False)
    created_at = Column(String, nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )
    category = relationship("Category", back_populates="tasks")

class Category(Base):

    __tablename__ = "categories"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(
        String,
        nullable=False
    )

    tasks = relationship("Task", back_populates="category")