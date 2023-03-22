"""commit

Revision ID: 6514b9ec8690
Revises: 9000e16781e2
Create Date: 2023-03-22 17:16:52.054386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6514b9ec8690'
down_revision = '9000e16781e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courses')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('title', sa.VARCHAR(length=199), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('teacher_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.id'], name='courses_teacher_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='courses_pkey'),
    sa.UniqueConstraint('id', name='courses_id_key')
    )
    # ### end Alembic commands ###
