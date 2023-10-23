"""Create temp for SystemStats

Revision ID: 882914182edc
Revises: d056e01bb0c8
Create Date: 2023-10-23 02:38:24.157365

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '882914182edc'
down_revision = 'd056e01bb0c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('system_stat', schema=None) as batch_op:
        batch_op.add_column(sa.Column('temperature', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('system_stat', schema=None) as batch_op:
        batch_op.drop_column('temperature')

    # ### end Alembic commands ###
