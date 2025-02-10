"""add likes

Revision ID: df695959d4b6
Revises: e6c9b18b5115
Create Date: 2025-02-10 09:28:04.931908

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df695959d4b6'
down_revision: Union[str, None] = 'e6c9b18b5115'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'comment', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='unique')
    op.drop_table('like')
    # ### end Alembic commands ###
