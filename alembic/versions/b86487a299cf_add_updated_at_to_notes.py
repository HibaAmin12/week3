"""add updated_at to notes

Revision ID: b86487a299cf
Revises: 269d6d126e0f
Create Date: 2026-08-04 18:57:44.055368
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "b86487a299cf"
down_revision = "269d6d126e0f"
branch_labels = None
depends_on = None


def upgrade():
    """
    Add the updated_at column to the notes table.
    """

    op.add_column(
        "notes",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade():
    """
    Remove the updated_at column from the notes table.
    """

    op.drop_column(
        "notes",
        "updated_at",
    )