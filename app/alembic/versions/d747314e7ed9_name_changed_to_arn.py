"""name changed to ARN

Revision ID: d747314e7ed9
Revises: 0d3c4fa7dbc3
Create Date: 2024-09-28 19:59:14.176217

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd747314e7ed9'
down_revision: Union[str, None] = '0d3c4fa7dbc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('containers', sa.Column('arn', sa.String(), nullable=True))
    op.drop_index('ix_containers_name', table_name='containers')
    op.create_index(op.f('ix_containers_arn'), 'containers', ['arn'], unique=False)
    op.drop_column('containers', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('containers', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_containers_arn'), table_name='containers')
    op.create_index('ix_containers_name', 'containers', ['name'], unique=False)
    op.drop_column('containers', 'arn')
    # ### end Alembic commands ###
