"""empty message

Revision ID: 8bbe8e55c02a
Revises: ea76a010cfeb
Create Date: 2022-05-03 17:31:20.499630

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '8bbe8e55c02a'
down_revision = 'ea76a010cfeb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('hash_text_question', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('document', 'hash_text_question')
    # ### end Alembic commands ###
