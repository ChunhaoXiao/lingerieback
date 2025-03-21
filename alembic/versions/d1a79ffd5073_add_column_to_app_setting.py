"""Add column to app_setting

Revision ID: d1a79ffd5073
Revises: e5ff8acd90c5
Create Date: 2025-03-20 23:31:46.731350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1a79ffd5073'
down_revision: Union[str, None] = 'e5ff8acd90c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('app_setting', sa.Column('options', sa.String(50), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('app_setting', 'options')
