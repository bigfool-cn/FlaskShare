"""empty message

Revision ID: 0f447d36e4ab
Revises: c354f3a39ebf
Create Date: 2018-03-09 16:14:16.880594

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0f447d36e4ab'
down_revision = 'c354f3a39ebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('attention_ibfk_2', 'attention', type_='foreignkey')
    op.drop_column('attention', 'user_id')
    op.add_column('user', sa.Column('attention_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'user', 'attention', ['attention_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'attention_id')
    op.add_column('attention', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('attention_ibfk_2', 'attention', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###
