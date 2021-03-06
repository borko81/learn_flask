"""empty message

Revision ID: f17aae77b661
Revises: 
Create Date: 2021-11-24 14:11:55.153541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f17aae77b661'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('complainers', 'iban')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('complainers', sa.Column('iban', sa.VARCHAR(length=22), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
