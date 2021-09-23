"""add investment transactions, multiple balance types

Revision ID: 4c2c226093a3
Revises: f09eb0ba1c57
Create Date: 2021-09-22 14:31:15.923446

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4c2c226093a3'
down_revision = 'f09eb0ba1c57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.drop_table('balances')
    op.add_column('plaid_items', sa.Column('status', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('plaid_items', 'status')
    op.create_table('balances',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('available', mysql.FLOAT(), nullable=True),
    sa.Column('current', mysql.FLOAT(), nullable=True),
    sa.Column('iso_currency_code', mysql.VARCHAR(length=8), nullable=True),
    sa.Column('timestamp', mysql.DATETIME(), nullable=True),
    sa.Column('account_id', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], name='balances_ibfk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('holding_balances')
    op.drop_table('investment_transactions')
    op.drop_table('account_balances')
    # ### end Alembic commands ###
