"""add posts table

Revision ID: c7e130d0ed06
Revises: dd183e87fb36
Create Date: 2022-04-10 09:27:28.355221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7e130d0ed06'
down_revision = 'dd183e87fb36'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
