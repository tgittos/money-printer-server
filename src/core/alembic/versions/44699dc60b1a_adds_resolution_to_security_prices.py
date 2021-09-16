"""adds resolution to security prices

Revision ID: 44699dc60b1a
Revises: 23ee869ccec1
Create Date: 2021-09-16 08:37:08.039168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44699dc60b1a'
down_revision = '23ee869ccec1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('security_prices', sa.Column('resolution', sa.String(length=32), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('security_prices', 'resolution')
    # ### end Alembic commands ###
