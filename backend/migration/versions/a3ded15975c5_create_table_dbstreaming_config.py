"""create table dbstreaming_config

Revision ID: a3ded15975c5
Revises: 9bccbd127e10
Create Date: 2021-10-11 20:19:54.891051

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = 'a3ded15975c5'
down_revision = '9bccbd127e10'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dbstreaming_config',
        sa.Column('id', sa.INTEGER, primary_key=True, index=True, autoincrement=True),
        sa.Column('name', sa.Enum('spark', 'mail', 'kafka', 'zalo', 'job_streaming', 'telegram'), nullable=False,
                  unique=True),
        sa.Column('value', sa.JSON, nullable=False),
    )


def downgrade():
    op.drop_table('dbstreaming_config')
