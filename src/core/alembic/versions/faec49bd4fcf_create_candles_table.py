"""create candles table

Revision ID: faec49bd4fcf
Revises: 
Create Date: 2021-03-24 23:03:49.636893

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faec49bd4fcf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'candles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('symbol', sa.String(10)),
        sa.Column('resolution', sa.String(3)),
        sa.Column('timestamp', sa.DateTime),
        sa.Column('open', sa.Float),
        sa.Column('close', sa.Float),
        sa.Column('high', sa.Float),
        sa.Column('low', sa.Float),
        sa.Column('volume', sa.Integer)
    )


def downgrade():
    op.drop_table('candles')
