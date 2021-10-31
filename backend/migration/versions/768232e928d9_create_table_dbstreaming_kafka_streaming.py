"""create table dbstreaming_kafka_streaming

Revision ID: 768232e928d9
Revises: a3ded15975c5
Create Date: 2021-10-13 11:00:19.336794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '768232e928d9'
down_revision = 'a3ded15975c5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'dbstreaming_kafka_streaming',
        sa.Column('id', sa.INTEGER, primary_key=True, index=True, autoincrement=True),
        sa.Column('topic_kafka', sa.VARCHAR(50), nullable=False),
        sa.Column('table_streaming', sa.VARCHAR(50), nullable=False),
        sa.UniqueConstraint('table_streaming')
    )


def downgrade():
    op.drop_table('dbstreaming_kafka_streaming')
