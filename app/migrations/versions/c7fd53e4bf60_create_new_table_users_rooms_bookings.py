"""Create new Table Users, Rooms, Bookings

Revision ID: c7fd53e4bf60
Revises: 0901cb7448d8
Create Date: 2023-10-09 12:52:21.541020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7fd53e4bf60'
down_revision: Union[str, None] = '0901cb7448d8'
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
