"""empty message

Revision ID: f8616fcd4438
Revises: 1bf6a35a5af9
Create Date: 2018-03-07 16:25:08.107148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8616fcd4438'
down_revision = '1bf6a35a5af9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('resource', sa.Column('img_url', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resource', 'img_url')
    # ### end Alembic commands ###
