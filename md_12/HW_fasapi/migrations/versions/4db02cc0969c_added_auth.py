"""Added auth

Revision ID: 4db02cc0969c
Revises: 04cbade1251b
Create Date: 2023-10-14 12:50:35.205833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4db02cc0969c'
down_revision: Union[str, None] = '04cbade1251b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=250), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('crated_at', sa.DateTime(), nullable=False),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('refresh_token', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.add_column('contacts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.alter_column('contacts', 'email',
               existing_type=sa.VARCHAR(length=70),
               nullable=True)
    op.alter_column('contacts', 'phone',
               existing_type=sa.VARCHAR(length=20),
               nullable=True)
    op.alter_column('contacts', 'birthday',
               existing_type=sa.DATE(),
               nullable=True)
    op.create_foreign_key(None, 'contacts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contacts', type_='foreignkey')
    op.alter_column('contacts', 'birthday',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('contacts', 'phone',
               existing_type=sa.VARCHAR(length=20),
               nullable=False)
    op.alter_column('contacts', 'email',
               existing_type=sa.VARCHAR(length=70),
               nullable=False)
    op.drop_column('contacts', 'user_id')
    op.drop_table('users')
    # ### end Alembic commands ###