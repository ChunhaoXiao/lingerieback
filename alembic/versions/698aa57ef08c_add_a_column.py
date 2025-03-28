"""Add a column

Revision ID: 698aa57ef08c
Revises: 
Create Date: 2025-03-27 20:46:10.911165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '698aa57ef08c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('app_setting', sa.Column('options', sa.String(500),nullable=True))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('app_setting', 'options')
