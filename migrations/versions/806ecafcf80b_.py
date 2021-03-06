"""empty message

Revision ID: 806ecafcf80b
Revises: a4d75d0152dd
Create Date: 2018-03-10 16:22:26.761468

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '806ecafcf80b'
down_revision = 'a4d75d0152dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('attention_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'resource', 'attention', ['attention_id'], ['id'])
    op.drop_constraint('user_ibfk_1', 'user', type_='foreignkey')
    op.drop_column('user', 'attention_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('attention_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('user_ibfk_1', 'user', 'attention', ['attention_id'], ['id'])
    op.drop_constraint(None, 'resource', type_='foreignkey')
    op.drop_column('resource', 'attention_id')
    # ### end Alembic commands ###
