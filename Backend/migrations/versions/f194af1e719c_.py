"""empty message

Revision ID: 9494af1e719c
Revises: eg46b0ae8fb1
Create Date: 2024-01-22 15:13:18.123091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f194af1e719c'
down_revision = 'eg46b0ae8fb1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_ProjectAPIKey')
    op.drop_table('tb_ProjectDataSet')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_ProjectDataSet',
    sa.Column('Project_DataSet_id', sa.INTEGER(), nullable=False),
    sa.Column('Pid', sa.INTEGER(), nullable=True),
    sa.Column('DSid', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['DSid'], ['tb_DataSet.DS_id'], ),
    sa.ForeignKeyConstraint(['Pid'], ['tb_Project.project_id'], ),
    sa.PrimaryKeyConstraint('Project_DataSet_id')
    )
    op.create_table('tb_ProjectAPIKey',
    sa.Column('Project_APIKey_id', sa.INTEGER(), nullable=False),
    sa.Column('Pid', sa.INTEGER(), nullable=True),
    sa.Column('AKid', sa.VARCHAR(length=30), nullable=True),
    sa.ForeignKeyConstraint(['AKid'], ['tb_APIKey.apiKey_id'], ),
    sa.ForeignKeyConstraint(['Pid'], ['tb_Project.project_id'], ),
    sa.PrimaryKeyConstraint('Project_APIKey_id')
    )
    # ### end Alembic commands ###
