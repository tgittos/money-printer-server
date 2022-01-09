"""empty message

Revision ID: 764d2e91d6e4
Revises: 
Create Date: 2022-01-08 19:01:16.187712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '764d2e91d6e4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_token_policies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doc', sa.String(length=10240), nullable=True),
    sa.Column('hosts', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.LargeBinary(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=True),
    sa.Column('last_name', sa.String(length=32), nullable=True),
    sa.Column('force_password_reset', sa.Boolean(), nullable=False),
    sa.Column('is_demo_profile', sa.Boolean(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('scheduled_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cron', sa.String(length=32), nullable=False),
    sa.Column('job_name', sa.String(length=128), nullable=False),
    sa.Column('json_args', sa.String(length=2048), nullable=True),
    sa.Column('last_run', sa.DateTime(), nullable=True),
    sa.Column('queue', sa.String(length=128), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('api_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('api_token_policy_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.LargeBinary(), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['api_token_policy_id'], ['api_token_policies.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('job_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scheduled_job_id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.String(length=128), nullable=False),
    sa.Column('success', sa.Boolean(), nullable=False),
    sa.Column('log', sa.String(length=5120), nullable=True),
    sa.Column('queue', sa.String(length=128), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['scheduled_job_id'], ['scheduled_jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('plaid_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.String(length=64), nullable=True),
    sa.Column('access_token', sa.String(length=64), nullable=True),
    sa.Column('request_id', sa.String(length=32), nullable=True),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reset_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('expiry', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('accounts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('plaid_item_id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('official_name', sa.String(length=256), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('subtype', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['plaid_item_id'], ['plaid_items.id'], ),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('account_balances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('available', sa.Float(), nullable=True),
    sa.Column('current', sa.Float(), nullable=True),
    sa.Column('iso_currency_code', sa.String(length=8), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('holdings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=64), nullable=True),
    sa.Column('cost_basis', sa.Float(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('iso_currency_code', sa.String(length=8), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('investment_transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=512), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('fees', sa.Float(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('investment_transaction_id', sa.String(length=256), nullable=True),
    sa.Column('iso_currency_code', sa.String(length=8), nullable=True),
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('subtype', sa.String(length=32), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('holding_balances',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('holding_id', sa.Integer(), nullable=False),
    sa.Column('cost_basis', sa.Float(), nullable=True),
    sa.Column('quantity', sa.Float(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['holding_id'], ['holdings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('holding_balances')
    op.drop_table('investment_transactions')
    op.drop_table('holdings')
    op.drop_table('account_balances')
    op.drop_table('accounts')
    op.drop_table('reset_tokens')
    op.drop_table('plaid_items')
    op.drop_table('job_results')
    op.drop_table('api_tokens')
    op.drop_table('scheduled_jobs')
    op.drop_table('profiles')
    op.drop_table('api_token_policies')
    # ### end Alembic commands ###
