"""setup

Revision ID: cfd8b1e79bed
Revises: 3268b0b6a51b
Create Date: 2021-07-21 13:49:09.205144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfd8b1e79bed'
down_revision = '3268b0b6a51b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('budget_category_analysis',
    sa.Column('category_name', sa.String(length=64), nullable=False),
    sa.Column('spending_this_month', sa.Float(), nullable=True),
    sa.Column('spending_this_month_perc', sa.Float(), nullable=True),
    sa.Column('spending_last_month', sa.Float(), nullable=True),
    sa.Column('spending_last_month_perc', sa.Float(), nullable=True),
    sa.Column('budgeting_this_month', sa.Float(), nullable=True),
    sa.Column('budgeting_this_month_perc', sa.Float(), nullable=True),
    sa.Column('budgeting_last_month', sa.Float(), nullable=True),
    sa.Column('budgeting_last_month_perc', sa.Float(), nullable=True),
    sa.Column('spending_diff_mom', sa.Float(), nullable=True),
    sa.Column('budgeting_diff_mom', sa.Float(), nullable=True),
    sa.Column('ideal_contribution', sa.Float(), nullable=True),
    sa.Column('ideal_contribution_perc', sa.Float(), nullable=True),
    sa.Column('spending_3m_diff', sa.Float(), nullable=True),
    sa.Column('budgeting_3m_diff', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('category_name')
    )
    with op.batch_alter_table('budget_category_analysis', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_budget_category_analysis_category_name'), ['category_name'], unique=True)

    op.create_table('budget_group_analysis',
    sa.Column('category_group_name', sa.String(length=64), nullable=False),
    sa.Column('spending_this_month', sa.Float(), nullable=True),
    sa.Column('spending_this_month_perc', sa.Float(), nullable=True),
    sa.Column('spending_last_month', sa.Float(), nullable=True),
    sa.Column('spending_last_month_perc', sa.Float(), nullable=True),
    sa.Column('budgeting_this_month', sa.Float(), nullable=True),
    sa.Column('budgeting_this_month_perc', sa.Float(), nullable=True),
    sa.Column('budgeting_last_month', sa.Float(), nullable=True),
    sa.Column('budgeting_last_month_perc', sa.Float(), nullable=True),
    sa.Column('spending_diff_mom', sa.Float(), nullable=True),
    sa.Column('budgeting_diff_mom', sa.Float(), nullable=True),
    sa.Column('ideal_contribution', sa.Float(), nullable=True),
    sa.Column('ideal_contribution_perc', sa.Float(), nullable=True),
    sa.Column('spending_3m_diff', sa.Float(), nullable=True),
    sa.Column('budgeting_3m_diff', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('category_group_name')
    )
    with op.batch_alter_table('budget_group_analysis', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_budget_group_analysis_category_group_name'), ['category_group_name'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('budget_group_analysis', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_budget_group_analysis_category_group_name'))

    op.drop_table('budget_group_analysis')
    with op.batch_alter_table('budget_category_analysis', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_budget_category_analysis_category_name'))

    op.drop_table('budget_category_analysis')
    # ### end Alembic commands ###
