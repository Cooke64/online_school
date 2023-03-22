"""commit

Revision ID: 62703964e88d
Revises: df236997f9b7
Create Date: 2023-03-22 17:08:11.124255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62703964e88d'
down_revision = 'df236997f9b7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('title', sa.String(length=199), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courses')
    # ### end Alembic commands ###
