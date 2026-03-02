"""Create generated_codes table

Revision ID: 001_create_generated_codes
Revises:
Create Date: 2026-02-28

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_create_generated_codes'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'generated_codes',
        sa.Column('code', sa.String(16), primary_key=True, nullable=False)
    )


def downgrade() -> None:
    op.drop_table('generated_codes')
