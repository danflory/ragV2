"""initial_schema

Revision ID: 35f8d079f4de
Revises: 
Create Date: 2026-01-07 21:36:06.916763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35f8d079f4de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.dialects import postgresql

def upgrade() -> None:
    # 1. history
    op.create_table(
        'history',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('role', sa.String(length=50), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('ghost_id', sa.String(length=100), server_default='unknown_ghost'),
        sa.Column('shell_id', sa.String(length=100), server_default='unknown_shell'),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.current_timestamp())
    )
    op.create_index('idx_history_timestamp', 'history', ['timestamp'])
    op.create_index('idx_history_ghost', 'history', ['ghost_id'])

    # 2. usage_stats
    op.create_table(
        'usage_stats',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('model', sa.String(length=100), nullable=True),
        sa.Column('layer', sa.String(length=10), nullable=True),
        sa.Column('prompt_tokens', sa.Integer(), nullable=True),
        sa.Column('completion_tokens', sa.Integer(), nullable=True),
        sa.Column('duration_ms', sa.Integer(), nullable=True)
    )
    op.create_index('idx_usage_timestamp', 'usage_stats', ['timestamp'])

    # 3. system_telemetry
    op.create_table(
        'system_telemetry',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('timestamp', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('component', sa.String(length=50), nullable=True),
        sa.Column('value', sa.Numeric(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True)
    )
    op.create_index('idx_telemetry_timestamp', 'system_telemetry', ['timestamp'])


def downgrade() -> None:
    op.drop_table('system_telemetry')
    op.drop_table('usage_stats')
    op.drop_table('history')
