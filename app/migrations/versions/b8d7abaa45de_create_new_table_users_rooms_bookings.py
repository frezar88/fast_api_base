"""Create new Table Users, Rooms, Bookings

Revision ID: b8d7abaa45de
Revises: 7a5656cd70c7
Create Date: 2023-10-09 13:34:16.492752

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b8d7abaa45de'
down_revision: Union[str, None] = '7a5656cd70c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
