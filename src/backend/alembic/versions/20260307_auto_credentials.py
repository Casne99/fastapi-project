"""create credentials table

Revision ID: 20260307_auto_credentials
Revises:
Create Date: 2026-03-07

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260307_auto_credentials'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'credentials',
        sa.Column('user', sa.String(length=255), nullable=False),
        sa.Column('password', sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint('user')
    )


def downgrade() -> None:
    op.drop_table('credentials')

