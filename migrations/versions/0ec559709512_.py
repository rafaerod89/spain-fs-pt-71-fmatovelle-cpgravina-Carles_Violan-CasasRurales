"""empty message

Revision ID: 0ec559709512
Revises: ee295f4a83eb
Create Date: 2024-08-30 10:08:01.605117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec559709512'
down_revision = 'ee295f4a83eb'
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
    op.drop_table('user')
    with op.batch_alter_table('traveler', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('traveler', schema=None) as batch_op:
        batch_op.drop_column('role')

    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('favorite_houses')
    # ### end Alembic commands ###