"""create blacklist table

Revision ID: 20260315_auto_blacklist
Revises: 20260307_auto_credentials
Create Date: 2026-03-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260315_auto_blacklist'
down_revision = '20260307_auto_credentials'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'blacklist',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['credentials.user']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('blacklist')
