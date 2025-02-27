"""merge heads

Revision ID: 72b0656f1bfd
Revises: 68def0585ebd, add_template_columns
Create Date: 2025-02-27 20:08:15.866592

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72b0656f1bfd'
down_revision: Union[str, None] = ('68def0585ebd', 'add_template_columns')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
