"""add template columns

Revision ID: add_template_columns
Revises: # you'll see the previous revision ID here
Create Date: 2024-02-26 17:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'add_template_columns'
down_revision: Union[str, None] = None  # replace with your previous revision
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add new columns to templates table
    op.add_column('templates', sa.Column('template_type', sa.String(), nullable=False, server_default='default'))
    op.add_column('templates', sa.Column('display_name', sa.String(), nullable=False, server_default='Untitled'))
    op.add_column('templates', sa.Column('fields', postgresql.JSONB(), nullable=True))
    op.add_column('templates', sa.Column('file_path', sa.String(), nullable=True))
    op.add_column('templates', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Add created_at and updated_at if they don't exist
    op.add_column('templates', sa.Column('created_at', sa.DateTime(timezone=True), 
                                       server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    op.add_column('templates', sa.Column('updated_at', sa.DateTime(timezone=True),
                                       server_default=sa.text('CURRENT_TIMESTAMP'), 
                                       onupdate=sa.text('CURRENT_TIMESTAMP'), nullable=False))


def downgrade() -> None:
    # Remove the columns in reverse order
    op.drop_column('templates', 'updated_at')
    op.drop_column('templates', 'created_at')
    op.drop_column('templates', 'user_id')
    op.drop_column('templates', 'file_path')
    op.drop_column('templates', 'fields')
    op.drop_column('templates', 'display_name')
    op.drop_column('templates', 'template_type') 