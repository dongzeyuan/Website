"""add markdown

Revision ID: 4936e3417e1d
Revises: be4ce66e2541
Create Date: 2018-05-08 21:03:02.460425

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4936e3417e1d'
down_revision = 'be4ce66e2541'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('body_html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'body_html')
    # ### end Alembic commands ###