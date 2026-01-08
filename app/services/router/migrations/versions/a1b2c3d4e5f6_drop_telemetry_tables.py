"""drop telemetry tables

Revision ID: a1b2c3d4e5f6
Revises: 35f8d079f4de
Create Date: 2026-01-08 16:35:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '35f8d079f4de'
branch_labels = None
depends_on = None


def upgrade():
    """
    Drop telemetry tables from router service.
    These tables are now owned by the dedicated telemetry service (RFC-002).
    """
    # Drop tables if they exist (safe migration)
    op.execute("DROP TABLE IF EXISTS system_telemetry CASCADE")
    op.execute("DROP TABLE IF EXISTS usage_stats CASCADE")


def downgrade():
    """
    Recreate telemetry tables (for rollback).
    Note: This will create empty tables. Historical data is not preserved.
    """
    # Recreate system_telemetry
    op.create_table(
        'system_telemetry',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('system_telemetry_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('event_type', sa.VARCHAR(length=50), nullable=False),
        sa.Column('component', sa.VARCHAR(length=100)),
        sa.Column('value', sa.FLOAT()),
        sa.Column('metadata', sa.JSON()),
        sa.Column('status', sa.VARCHAR(length=20)),
        sa.Column('timestamp', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_telemetry_timestamp', 'system_telemetry', ['timestamp'])
    
    # Recreate usage_stats
    op.create_table(
        'usage_stats',
        sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('usage_stats_id_seq'::regclass)"), autoincrement=True, nullable=False),
        sa.Column('ghost_id', sa.VARCHAR(length=100)),
        sa.Column('shell_id', sa.VARCHAR(length=100)),
        sa.Column('model_name', sa.VARCHAR(length=100)),
        sa.Column('tokens_input', sa.INTEGER()),
        sa.Column('tokens_output', sa.INTEGER()),
        sa.Column('cost_usd', sa.FLOAT()),
        sa.Column('timestamp', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
