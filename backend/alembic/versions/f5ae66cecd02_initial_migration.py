"""Initial migration

Revision ID: f5ae66cecd02
Revises: 84ac63aeb1e4
Create Date: 2024-12-23 13:37:45.951402

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5ae66cecd02'
down_revision: Union[str, None] = '84ac63aeb1e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('course_code', sa.String(length=10), nullable=False),
    sa.Column('semester', sa.String(length=10), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('_id'),
    sa.UniqueConstraint('course_code')
    )
    op.create_table('users',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('google_sub', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('google_sub')
    )
    op.create_table('topics',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses._id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('_id')
    )
    op.create_table('notes',
    sa.Column('_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('pdf_url', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('topic_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['topic_id'], ['topics._id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users._id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notes')
    op.drop_table('topics')
    op.drop_table('users')
    op.drop_table('courses')
    # ### end Alembic commands ###
