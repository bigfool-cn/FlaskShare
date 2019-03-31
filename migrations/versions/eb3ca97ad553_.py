"""empty message

Revision ID: eb3ca97ad553
Revises: 90a36670be49
Create Date: 2018-02-28 14:55:42.467203

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'eb3ca97ad553'
down_revision = '90a36670be49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resource', 'rs_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('rs_type', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
