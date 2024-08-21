"""empty message

Revision ID: 6e5dd2128af0
Revises: fb7d2ddaadef
Create Date: 2024-08-21 09:02:24.588103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e5dd2128af0'
down_revision = 'fb7d2ddaadef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('traveler',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userName', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('favorite', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('userName')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('traveler')
    # ### end Alembic commands ###