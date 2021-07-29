"""Add question_number to User model

Revision ID: 0cb2952141a2
Revises: 134a669901ab
Create Date: 2021-07-29 21:32:34.303725

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '0cb2952141a2'
down_revision = '134a669901ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('decrypto_user', sa.Column('question_number', sa.Integer(), nullable=False, server_default='1'))
    op.alter_column('decrypto_user', 'question_number', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('decrypto_user', 'question_number')
    # ### end Alembic commands ###
