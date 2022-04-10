"""add content column to post

Revision ID: 1ff4ffe9ef87
Revises: c7e130d0ed06
Create Date: 2022-04-10 09:29:42.898556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ff4ffe9ef87'
down_revision = 'c7e130d0ed06'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
