"""empty message

Revision ID: 74d5fec10103
Revises: 18fda47cebe1
Create Date: 2019-04-08 19:43:40.660445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74d5fec10103'
down_revision = '18fda47cebe1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('chat', 'topic')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat', sa.Column('topic', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###