"""refactoring background job system

Revision ID: 56478b8526b5
Revises: 4debdd6f0f8b
Create Date: 2021-10-19 12:53:22.430781

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '56478b8526b5'
down_revision = '4debdd6f0f8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.String(length=128), nullable=False),
    sa.Column('success', sa.Boolean(), nullable=False),
    sa.Column('log', sa.String(length=5120), nullable=True),
    sa.Column('queue', sa.String(length=128), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('profiles', sa.Column('is_admin', sa.Boolean(), nullable=False))
    op.add_column('scheduled_jobs', sa.Column('cron', sa.String(length=32), nullable=False))
    op.add_column('scheduled_jobs', sa.Column('queue', sa.String(length=128), nullable=False))
    op.add_column('scheduled_jobs', sa.Column('active', sa.Boolean(), nullable=False))
    op.drop_column('scheduled_jobs', 'frequency_value')
    op.drop_column('scheduled_jobs', 'frequency_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('scheduled_jobs', sa.Column('frequency_type', mysql.VARCHAR(length=64), nullable=False))
    op.add_column('scheduled_jobs', sa.Column('frequency_value', mysql.VARCHAR(length=32), nullable=False))
    op.drop_column('scheduled_jobs', 'active')
    op.drop_column('scheduled_jobs', 'queue')
    op.drop_column('scheduled_jobs', 'cron')
    op.drop_column('profiles', 'is_admin')
    op.drop_table('job_results')
    # ### end Alembic commands ###