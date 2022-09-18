"""Added initial tables

Revision ID: b537d67e4227
Revises: 
Create Date: 2022-09-18 15:08:40.227613

"""
import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision = 'b537d67e4227'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sessions_chat_id'), 'sessions', ['chat_id'], unique=True)
    op.create_table('gamestates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('current_question_id', sa.Integer(), nullable=False),
    sa.Column('current_player', sa.Integer(), nullable=False),
    sa.Column('state', sa.Enum('WAIT_FOR_SELECT_GAME', 'WAIT_FOR_PLAYERS', 'WAIT_FOR_PLAYER_ACTION', 'WAIT_FOR_PLAYER_ANSWER', name='gamestateenum'), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('players',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('pot', sa.Integer(), nullable=False),
    sa.Column('is_answered', sa.Boolean(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_players_telegram_id'), 'players', ['telegram_id'], unique=False)
    op.create_table('questionsessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('questionsessions')
    op.drop_index(op.f('ix_players_telegram_id'), table_name='players')
    op.drop_table('players')
    op.drop_table('gamestates')
    op.drop_index(op.f('ix_sessions_chat_id'), table_name='sessions')
    op.drop_table('sessions')
    # ### end Alembic commands ###