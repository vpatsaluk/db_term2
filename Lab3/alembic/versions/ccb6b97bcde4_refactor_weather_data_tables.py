"""Refactor weather data tables

Revision ID: ccb6b97bcde4
Revises: b991e1e0150b
Create Date: 2024-04-15 13:29:59.318221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccb6b97bcde4'
down_revision: Union[str, None] = 'b991e1e0150b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    INSERT INTO precip_data(id, precip_mm, precip_in)
    SELECT id, precip_mm, precip_in FROM weather_data
    """)


def downgrade() -> None:
    op.drop_table('precip_data')
