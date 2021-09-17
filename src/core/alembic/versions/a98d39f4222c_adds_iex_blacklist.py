"""adds iex blacklist

Revision ID: a98d39f4222c
Revises: 44699dc60b1a
Create Date: 2021-09-17 13:39:06.130436

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a98d39f4222c'
down_revision = '44699dc60b1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('iex_blacklists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=265), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('iex_blacklists')
    # ### end Alembic commands ###
