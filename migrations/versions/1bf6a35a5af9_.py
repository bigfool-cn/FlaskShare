"""empty message

Revision ID: 1bf6a35a5af9
Revises: eb3ca97ad553
Create Date: 2018-02-28 14:58:57.815455

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1bf6a35a5af9'
down_revision = 'eb3ca97ad553'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_link_addtime'), 'link', ['addtime'], unique=False)
    op.add_column('resource', sa.Column('link_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'resource', 'link', ['link_id'], ['id'])
    op.drop_column('resource', 'url_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('url_type', mysql.TEXT(), nullable=True))
    op.drop_constraint(None, 'resource', type_='foreignkey')
    op.drop_column('resource', 'link_id')
    op.drop_index(op.f('ix_link_addtime'), table_name='link')
    op.drop_table('link')
    # ### end Alembic commands ###
