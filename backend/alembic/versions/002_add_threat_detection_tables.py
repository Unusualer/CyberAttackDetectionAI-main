"""add threat detection tables

Revision ID: 002
Revises: 001
Create Date: 2024-01-20 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create threat_events table
    op.create_table(
        'threat_events',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('timestamp', sa.DateTime, nullable=False),
        sa.Column('threat_type', sa.String(50), nullable=False),
        sa.Column('severity', sa.String(20), nullable=False),
        sa.Column('source_ip', sa.String(45)),
        sa.Column('details', sa.JSON),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('organization_id', sa.String(36), nullable=False)
    )

def downgrade():
    op.drop_table('threat_events') 