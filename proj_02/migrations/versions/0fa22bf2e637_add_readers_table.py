"""add readers table

Revision ID: 0fa22bf2e637
Revises: 2821e1a90198
Create Date: 2022-10-17 19:06:49.632471

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0fa22bf2e637'
down_revision = '2821e1a90198'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('readers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('books', sa.Column('reader_id', sa.Integer(), nullable=False))
    op.create_index(op.f('ix_books_reader_id'), 'books', ['reader_id'], unique=False)
    op.create_foreign_key(None, 'books', 'readers', ['reader_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books', type_='foreignkey')
    op.drop_index(op.f('ix_books_reader_id'), table_name='books')
    op.drop_column('books', 'reader_id')
    op.drop_table('readers')
    # ### end Alembic commands ###
