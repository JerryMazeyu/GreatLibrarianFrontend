"""empty message

Revision ID: df499f3796cb
Revises: 940427fe1718
Create Date: 2023-12-22 11:27:56.851262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df499f3796cb'
down_revision = '940427fe1718'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_QA')
    op.drop_table('tb_TestProject')
    op.drop_table('_alembic_tmp_tb_Project')
    with op.batch_alter_table('tb_Project', schema=None) as batch_op:
        batch_op.drop_column('project_DataSet')
        batch_op.drop_column('project_LLM')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tb_Project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('project_LLM', sa.VARCHAR(length=200), nullable=True))
        batch_op.add_column(sa.Column('project_DataSet', sa.VARCHAR(length=200), nullable=True))

    op.create_table('_alembic_tmp_tb_Project',
    sa.Column('project_id', sa.INTEGER(), nullable=False),
    sa.Column('project_name', sa.VARCHAR(length=80), nullable=True),
    sa.Column('project_info', sa.VARCHAR(length=200), nullable=True),
    sa.Column('userId', sa.VARCHAR(length=30), nullable=True),
    sa.ForeignKeyConstraint(['userId'], ['tb_user.user_id'], ),
    sa.PrimaryKeyConstraint('project_id')
    )
    op.create_table('tb_TestProject',
    sa.Column('testProject_id', sa.VARCHAR(length=30), nullable=False),
    sa.Column('testProject_time', sa.DATETIME(), nullable=True),
    sa.Column('testProject_LLMs', sa.VARCHAR(length=100), nullable=True),
    sa.Column('testProject_dataSet', sa.VARCHAR(length=100), nullable=True),
    sa.Column('projectId', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['projectId'], ['tb_Project.project_id'], ),
    sa.PrimaryKeyConstraint('testProject_id')
    )
    op.create_table('tb_QA',
    sa.Column('QA_id', sa.INTEGER(), nullable=False),
    sa.Column('QA_time', sa.DATETIME(), nullable=True),
    sa.Column('QA_question', sa.VARCHAR(length=80), nullable=True),
    sa.Column('QA_answer', sa.VARCHAR(length=200), nullable=True),
    sa.Column('QA_score', sa.FLOAT(), nullable=True),
    sa.Column('QA_thread', sa.INTEGER(), nullable=True),
    sa.Column('TPid', sa.VARCHAR(length=30), nullable=True),
    sa.ForeignKeyConstraint(['TPid'], ['tb_TestProject.tP_id'], ),
    sa.PrimaryKeyConstraint('QA_id')
    )
    # ### end Alembic commands ###
