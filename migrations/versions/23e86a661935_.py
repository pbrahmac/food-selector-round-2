"""empty message

Revision ID: 23e86a661935
Revises: c3accced8389
Create Date: 2019-05-26 23:55:12.144400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23e86a661935'
down_revision = 'c3accced8389'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('firstname', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('lastname', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'lastname')
    op.drop_column('users', 'firstname')
    # ### end Alembic commands ###
