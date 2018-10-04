"""Remove recipient_id column from post_comment

Revision ID: e423b2f745a1
Revises: e2912906eb86
Create Date: 2018-10-02 20:06:28.687373

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e423b2f745a1'
down_revision = 'e2912906eb86'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('post_comment_ibfk_3', 'post_comment', type_='foreignkey')
    op.drop_column('post_comment', 'recipient_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_comment', sa.Column('recipient_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('post_comment_ibfk_3', 'post_comment', 'user', ['recipient_id'], ['id'])
    # ### end Alembic commands ###