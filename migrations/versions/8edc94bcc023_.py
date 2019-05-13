"""empty message

Revision ID: 8edc94bcc023
Revises: 74d5fec10103
Create Date: 2019-05-06 12:47:14.845261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8edc94bcc023'
down_revision = '74d5fec10103'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('topic', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat', 'topic')
    # ### end Alembic commands ###
