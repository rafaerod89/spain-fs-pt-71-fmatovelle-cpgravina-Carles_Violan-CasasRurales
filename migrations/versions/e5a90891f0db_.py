"""empty message

Revision ID: e5a90891f0db
Revises: 5820517e5fa4
Create Date: 2024-08-30 04:44:25.660524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a90891f0db'
down_revision = '5820517e5fa4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('favorite_houses',
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('traveler_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['house_id'], ['house.id'], ),
    sa.ForeignKeyConstraint(['traveler_id'], ['traveler.id'], ),
    sa.PrimaryKeyConstraint('house_id', 'traveler_id')
    )
    with op.batch_alter_table('traveler', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('traveler', schema=None) as batch_op:
        batch_op.drop_column('role')

    op.drop_table('favorite_houses')
    # ### end Alembic commands ###