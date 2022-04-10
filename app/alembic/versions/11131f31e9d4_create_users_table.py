"""create Users table

Revision ID: 11131f31e9d4
Revises: 1ff4ffe9ef87
Create Date: 2022-04-10 09:40:39.998289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11131f31e9d4'
down_revision = '1ff4ffe9ef87'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email')
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
