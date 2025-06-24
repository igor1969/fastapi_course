"""add users

Revision ID: 054af93601e2
Revises: ab36b582d983
Create Date: 2025-06-17 21:23:29.644213

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "054af93601e2"
down_revision: Union[str, None] = "ab36b582d983"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
