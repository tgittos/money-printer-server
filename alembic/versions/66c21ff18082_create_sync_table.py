"""create sync table

Revision ID: 66c21ff18082
Revises: faec49bd4fcf
Create Date: 2021-03-29 18:55:18.960864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66c21ff18082'
down_revision = 'faec49bd4fcf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'sync',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('symbol', sa.String(10)),
        sa.Column('last_update', sa.DateTime)
    )


def downgrade():
    op.drop_table('sync')
