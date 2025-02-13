"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-20 09:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create organizations table
    op.create_table(
        'organizations',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('api_key', sa.String(64), unique=True, nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('settings', sa.JSON)
    )

    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('is_superuser', sa.Boolean(), default=False),
        sa.Column('organization_id', sa.String(36), sa.ForeignKey('organizations.id')),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

    # Create ML models table
    op.create_table(
        'ml_models',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('version', sa.String(20), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('metrics', sa.JSON),
        sa.Column('last_trained', sa.DateTime()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

def downgrade():
    op.drop_table('ml_models')
    op.drop_table('users')
    op.drop_table('organizations') 