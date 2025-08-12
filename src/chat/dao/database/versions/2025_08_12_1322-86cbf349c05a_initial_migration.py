"""Initial migration

Revision ID: 86cbf349c05a
Revises: 
Create Date: 2025-08-12 13:22:15.581457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from config import DB_CONFIG


# revision identifiers, used by Alembic.
revision: str = '86cbf349c05a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute(f'CREATE SCHEMA IF NOT EXISTS {DB_CONFIG.schema}')

    op.create_table('session',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_session')),
        schema='help_desk_ai',
    )
    op.create_table('message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.Integer(), nullable=False),
        sa.Column('role', sa.Enum('SYSTEM', 'USER', 'ASSISTANT', name='message_role_enum', create_type=False), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['help_desk_ai.session.id'], name=op.f('fk_message_session_id_session')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_message')),
        schema='help_desk_ai',
    )


def downgrade() -> None:

    op.drop_table('message', schema='help_desk_ai')
    op.drop_table('session', schema='help_desk_ai')

    op.execute('DROP TYPE IF EXISTS message_role_enum')

    op.execute(f'DROP SCHEMA IF EXISTS {DB_CONFIG.schema}')
