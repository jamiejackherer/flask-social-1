"""Testing altering columns

Revision ID: d7283dda6635
Revises: 8506b6ebae9e
Create Date: 2018-09-29 20:50:55.066768

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd7283dda6635'
down_revision = '8506b6ebae9e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notification', sa.Column('active', sa.Boolean(), nullable=False))
    op.add_column('notification', sa.Column('deleted', sa.DateTime(), nullable=True))
    op.add_column('notification', sa.Column('updated', sa.DateTime(), nullable=False))
    op.alter_column('notification', 'created',
               existing_type=mysql.FLOAT(),
               nullable=False)
    op.drop_index('ix_notification_created', table_name='notification')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_notification_created', 'notification', ['created'], unique=False)
    op.alter_column('notification', 'created',
               existing_type=mysql.FLOAT(),
               nullable=True)
    op.drop_column('notification', 'updated')
    op.drop_column('notification', 'deleted')
    op.drop_column('notification', 'active')
    # ### end Alembic commands ###
