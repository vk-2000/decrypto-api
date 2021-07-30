"""Add rank and question_number_updated_at to User model

Revision ID: faedc202f5e2
Revises: 0cb2952141a2
Create Date: 2021-07-30 15:28:14.534123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faedc202f5e2'
down_revision = '0cb2952141a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # Set `server_default` for records already in table
    op.add_column('decrypto_user', sa.Column('question_number_updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()))
    op.add_column('decrypto_user', sa.Column('rank', sa.Integer(), nullable=False, server_default='0'))

    # Remove `server_default` as client will provide defaults for new records
    op.alter_column('decrypto_user', 'question_number_updated_at', server_default=None)
    op.alter_column('decrypto_user', 'rank', server_default=None)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('decrypto_user', 'rank')
    op.drop_column('decrypto_user', 'question_number_updated_at')
    # ### end Alembic commands ###