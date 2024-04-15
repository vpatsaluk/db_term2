"""add col wind_data

Revision ID: 048fbe07dc89
Revises: ccb6b97bcde4
Create Date: 2024-04-15 13:35:26.605682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '048fbe07dc89'
down_revision: Union[str, None] = 'ccb6b97bcde4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('wind_data', sa.Column('is_it_safe_to_go_out', sa.Boolean(), nullable=True,
                 server_default=sa.text('False')))
    op.execute("""
    UPDATE wind_data
    SET is_it_safe_to_go_out = (wind_speed_kph < 10)
    """)

def downgrade() -> None:
    op.drop_column('wind_data', 'is_it_safe_to_go_out')
