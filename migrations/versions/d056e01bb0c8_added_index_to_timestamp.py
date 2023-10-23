"""Added index to timestamp

Revision ID: d056e01bb0c8
Revises: 
Create Date: 2023-10-23 02:32:19.761205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd056e01bb0c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_event_timestamp'), ['timestamp'], unique=False)

    with op.batch_alter_table('system_stat', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_system_stat_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('system_stat', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_system_stat_timestamp'))

    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_event_timestamp'))

    # ### end Alembic commands ###
