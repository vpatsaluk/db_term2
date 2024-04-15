import pandas as pd

df = pd.read_csv('GlobalWeatherRepository.csv')


for col in df.columns:
    print(col)


"""Refactor weather data tables

Revision ID: 02ee42867683
Revises: b991e1e0150b
Create Date: 2024-04-15 12:08:12.766424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02ee42867683'
down_revision: Union[str, None] = 'b991e1e0150b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.create_table('wind_data',
    #     sa.Column('id', sa.Integer(), nullable=False),
    #     sa.Column('wind_speed_kph', sa.Float(), nullable=True),
    #     sa.Column('wind_speed_mph', sa.Float(), nullable=True),
    #     sa.Column('wind_direction', sa.String(length=50), nullable=True),
    #     sa.Column('is_it_safe_to_go_out', sa.Boolean(), nullable=True),
    #     sa.PrimaryKeyConstraint('id')
    # )
    # Перемістіть дані зі старої таблиці в нову
    op.execute("""
    INSERT INTO wind_data(id, wind_speed_kph, wind_speed_mph, wind_direction, is_it_safe_to_go_out)
    SELECT id, wind_speed_kph, wind_speed_mph, wind_direction, is_it_safe_to_go_out FROM weather_data
    """)
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wind_data')
    # ### end Alembic commands ###

"""create initial tables

Revision ID: b991e1e0150b
Revises: 
Create Date: 2024-04-15 12:05:32.211478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b991e1e0150b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, "wind_data"):
        op.create_table('wind_data',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('wind_speed_kph', sa.Float(), nullable=True),
            sa.Column('wind_speed_mph', sa.Float(), nullable=True),
            sa.Column('wind_direction', sa.String(length=50), nullable=True),
            sa.Column('is_it_safe_to_go_out', sa.Boolean(), nullable=True),
            sa.PrimaryKeyConstraint('id')
        )
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wind_data')
    # ### end Alembic commands ###
