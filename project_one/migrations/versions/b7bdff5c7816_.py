"""empty message

Revision ID: b7bdff5c7816
Revises: 0954339f4ecb
Create Date: 2021-11-12 16:34:05.552101

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7bdff5c7816'
down_revision = '0954339f4ecb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('shop_model')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shop_model',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('shop')
    # ### end Alembic commands ###
