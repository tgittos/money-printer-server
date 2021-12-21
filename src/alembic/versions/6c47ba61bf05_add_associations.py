"""Add associations

Revision ID: 6c47ba61bf05
Revises: 56478b8526b5
Create Date: 2021-12-21 16:50:15.498835

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6c47ba61bf05'
down_revision = '56478b8526b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_results', sa.Column('scheduled_job_id', sa.Integer(), nullable=False))
    op.drop_column('job_results', 'job_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job_results', sa.Column('job_id', mysql.VARCHAR(length=128), nullable=False))
    op.drop_column('job_results', 'scheduled_job_id')
    # ### end Alembic commands ###
