"""empty message

Revision ID: 61deffa27b6f
Revises: 50d577a0642e
Create Date: 2023-12-11 23:13:08.469738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61deffa27b6f'
down_revision = '50d577a0642e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tb_friendship',
    sa.Column('fs_Id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('userid', sa.String(length=30), nullable=False),
    sa.Column('friend_token', sa.String(length=30), nullable=False),
    sa.Column('friend_state', sa.Integer(), nullable=False),
    sa.Column('createTime', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['userid'], ['tb_user.user_id'], ),
    sa.PrimaryKeyConstraint('fs_Id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_friendship')
    # ### end Alembic commands ###