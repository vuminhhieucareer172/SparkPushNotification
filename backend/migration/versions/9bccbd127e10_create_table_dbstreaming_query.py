"""create table dbstreaming_job_stream

Revision ID: 9bccbd127e10
Revises: 
Create Date: 2021-10-07 12:22:23.297192

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = '9bccbd127e10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dbstreaming_query',
        sa.Column('id', sa.INTEGER, primary_key=True, index=True, autoincrement=True),
        sa.Column('sql', sa.VARCHAR(50), nullable=False),
        sa.Column('topic_kafka_output', sa.VARCHAR(50), nullable=False),
        sa.Column('time_trigger', sa.VARCHAR(50), nullable=False, server_default='1 second'),
        sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, nullable=False, server_default=sa.func.now(), server_onupdate=sa.func.now()),
        sa.Column('contact', sa.JSON, nullable=True),
    )


def downgrade():
    op.drop_table('dbstreaming_query')
