"""initial_schema

Revision ID: c6b1b8a06e4c
Revises: 
Create Date: 2026-01-07 21:34:50.818384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c6b1b8a06e4c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use op.create_table but handle existing table if any (Alembic usually expects clean slate)
    # Since we are moving from init_schema() to Alembic, we assume starting clean or 
    # the user will run 'alembic stamp head' if tables already exist.
    op.create_table(
        'audit_log',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('ghost_id', sa.String(length=100), nullable=False),
        sa.Column('shell_id', sa.String(length=100), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('resource', sa.String(length=255), nullable=False),
        sa.Column('result', sa.String(length=20), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('metadata', sa.Text(), nullable=True)
    )
    op.create_index('idx_audit_timestamp', 'audit_log', ['timestamp'])
    op.create_index('idx_audit_ghost', 'audit_log', ['ghost_id'])


def downgrade() -> None:
    op.drop_table('audit_log')
