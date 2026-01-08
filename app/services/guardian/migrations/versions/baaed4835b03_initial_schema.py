"""initial_schema

Revision ID: baaed4835b03
Revises: 
Create Date: 2026-01-07 21:35:45.655055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'baaed4835b03'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'agent_badges',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ghost_id', sa.String(length=100), nullable=False),
        sa.Column('badge_name', sa.String(length=100), nullable=False),
        sa.Column('granted_at', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.UniqueConstraint('ghost_id', 'badge_name')
    )
    op.create_index('idx_badges_ghost', 'agent_badges', ['ghost_id'])


def downgrade() -> None:
    op.drop_table('agent_badges')
