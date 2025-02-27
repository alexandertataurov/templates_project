"""drop name column from templates

Revision ID: a9bcecbb3306
Revises: 50585783a30b
Create Date: 2025-02-27 20:13:20.536791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9bcecbb3306'
down_revision: Union[str, None] = '50585783a30b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Drop the "name" column from the "templates" table
    op.drop_column('templates', 'name')

def downgrade():
    # Add the "name" column back as nullable (optional rollback step)
    op.add_column('templates', sa.Column('name', sa.String(length=255), nullable=True))