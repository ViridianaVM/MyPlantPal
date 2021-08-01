"""empty message

Revision ID: 31c3f20bc2fe
Revises: 
Create Date: 2021-07-30 22:54:34.607353

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31c3f20bc2fe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('token_id', sa.String(length=415), nullable=False),
    sa.Column('device_id', sa.String(length=415), nullable=True),
    sa.PrimaryKeyConstraint('token_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###