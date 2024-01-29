"""Create trigger on students table

Revision ID: c225d02ca6bb
Revises: 
Create Date: 2024-01-26 20:08:03.454686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c225d02ca6bb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(sa.DDL(
        "alter table users rename column tg_id to chat_id;"
    ))


def downgrade() -> None:
    pass
