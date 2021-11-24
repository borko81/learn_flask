"""empty message

Revision ID: 7ff119b5d456
Revises: 
Create Date: 2021-11-24 16:40:49.591944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ff119b5d456'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('park', sa.Column('name', sa.String(length=20), nullable=False))
    op.add_column('park', sa.Column('get_in', sa.DateTime(), nullable=False))
    op.add_column('park', sa.Column('get_out', sa.DateTime(), nullable=True))
    op.add_column('park', sa.Column('tax', sa.Integer(), nullable=True))
    op.add_column('park', sa.Column('pay', sa.Boolean(), nullable=True))
    op.add_column('prices', sa.Column('stay_time', sa.String(length=10), nullable=False))
    op.add_column('prices', sa.Column('price', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('prices', 'price')
    op.drop_column('prices', 'stay_time')
    op.drop_column('park', 'pay')
    op.drop_column('park', 'tax')
    op.drop_column('park', 'get_out')
    op.drop_column('park', 'get_in')
    op.drop_column('park', 'name')
    # ### end Alembic commands ###
