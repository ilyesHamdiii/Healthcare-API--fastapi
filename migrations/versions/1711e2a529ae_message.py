"""message

Revision ID: 1711e2a529ae
Revises: 35d5c3b2dd9c
Create Date: 2025-09-07 16:57:28.829264

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1711e2a529ae'
down_revision: Union[str, Sequence[str], None] = '35d5c3b2dd9c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
