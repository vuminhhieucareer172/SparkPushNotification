"""create table dbstreaming_job_stream

Revision ID: 9bccbd127e10
Revises: 
Create Date: 2021-10-07 12:22:23.297192

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy.dialects.mysql import LONGTEXT

revision = '9bccbd127e10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dbstreaming_job_stream',
        sa.Column('id', sa.INTEGER, primary_key=True, index=True, autoincrement=True),
        sa.Column('job_name', sa.VARCHAR(50), nullable=False),
        sa.Column('config', sa.VARCHAR(255), nullable=False),
        sa.Column('status', sa.Enum('RUNNING', 'STOP', 'ERROR'), nullable=False, server_default='RUNNING'),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default=sa.sql.true()),
        sa.Column('time', sa.VARCHAR(50), nullable=False, server_default='0 0 * * *'),
        sa.Column('template', sa.VARCHAR(255), nullable=False),
        sa.Column('log', LONGTEXT),
        mysql_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci'
    )


def downgrade():
    op.drop_table('dbstreaming_job_stream')
