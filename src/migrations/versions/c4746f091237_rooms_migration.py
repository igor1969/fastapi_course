"""rooms migration

Revision ID: c4746f091237
Revises: 80c336f154ec
Create Date: 2025-03-29 20:33:08.418914

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4746f091237'
down_revision: Union[str, None] = '80c336f154ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass