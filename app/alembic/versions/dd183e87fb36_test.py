"""test

Revision ID: dd183e87fb36
Revises: 
Create Date: 2022-04-09 12:56:45.383053

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dd183e87fb36'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('testtable', sa.Column('testcolumn', sa.Integer, nullable=False, primary_key=True))
    pass


def downgrade():
    op.drop_table('test')
    pass
