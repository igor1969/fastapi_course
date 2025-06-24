"""unique email added

Revision ID: ed83b981ccd0
Revises: 054af93601e2
Create Date: 2025-06-19 12:24:04.391806

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ed83b981ccd0"
down_revision: Union[str, None] = "054af93601e2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
