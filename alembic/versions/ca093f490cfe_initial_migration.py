"""initial migration

Revision ID: ca093f490cfe
Revises: 
Create Date: 2023-11-08 18:56:17.245275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca093f490cfe'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )

    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String)
    )

    op.create_table(
        'students',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id')),
        sa.Index('idx_group_id', 'group_id') 
    )

    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('teacher_id', sa.Integer, sa.ForeignKey('teachers.id')),
        sa.Index('idx_teacher_id', 'teacher_id') 
    )

    op.create_table(
        'grades',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('student_id', sa.Integer, sa.ForeignKey('students.id')),
        sa.Column('subject_id', sa.Integer, sa.ForeignKey('subjects.id')),
        sa.Column('grade', sa.Integer),
        sa.Column('date', sa.Date),
        sa.Index('idx_student_id', 'student_id'),  
        sa.Index('idx_subject_id', 'subject_id')   
        
    )

def downgrade():
    op.drop_table('grades')
    op.drop_table('subjects')
    op.drop_table('teachers')
    op.drop_table('students')
    op.drop_table('groups')

