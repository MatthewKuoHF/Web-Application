"""enroll_lists table

Revision ID: 32e4372466f5
Revises: 1c149625c7dc
Create Date: 2019-01-29 14:47:58.121620

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32e4372466f5'
down_revision = '1c149625c7dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sqlite_sequence')
    op.alter_column('course', 'department',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('course', 'name',
               existing_type=sa.TEXT(),
               nullable=True)
    op.alter_column('course', 'time1',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('course', 'time2',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_course_department'), 'course', ['department'], unique=False)
    op.create_index(op.f('ix_course_name'), 'course', ['name'], unique=False)
    op.create_index(op.f('ix_course_time1'), 'course', ['time1'], unique=False)
    op.create_index(op.f('ix_course_time2'), 'course', ['time2'], unique=False)
    op.create_foreign_key(None, 'course', 'user', ['time2'], ['id'])
    op.drop_column('course', 'student')
    op.alter_column('enroll_list', 'cid',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('enroll_list', 'sid',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_index(op.f('ix_enroll_list_cid'), 'enroll_list', ['cid'], unique=False)
    op.create_index(op.f('ix_enroll_list_sid'), 'enroll_list', ['sid'], unique=False)
    op.create_index(op.f('ix_user_address1'), 'user', ['address1'], unique=False)
    op.create_index(op.f('ix_user_address2'), 'user', ['address2'], unique=False)
    op.create_index(op.f('ix_user_city'), 'user', ['city'], unique=False)
    op.create_index(op.f('ix_user_fname'), 'user', ['fname'], unique=False)
    op.create_index(op.f('ix_user_lname'), 'user', ['lname'], unique=False)
    op.create_index(op.f('ix_user_state'), 'user', ['state'], unique=False)
    op.create_index(op.f('ix_user_zip'), 'user', ['zip'], unique=False)
    op.drop_column('user', 'department')
    op.drop_column('user', 'degree')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('degree', sa.TEXT(), nullable=True))
    op.add_column('user', sa.Column('department', sa.TEXT(), nullable=True))
    op.drop_index(op.f('ix_user_zip'), table_name='user')
    op.drop_index(op.f('ix_user_state'), table_name='user')
    op.drop_index(op.f('ix_user_lname'), table_name='user')
    op.drop_index(op.f('ix_user_fname'), table_name='user')
    op.drop_index(op.f('ix_user_city'), table_name='user')
    op.drop_index(op.f('ix_user_address2'), table_name='user')
    op.drop_index(op.f('ix_user_address1'), table_name='user')
    op.drop_index(op.f('ix_enroll_list_sid'), table_name='enroll_list')
    op.drop_index(op.f('ix_enroll_list_cid'), table_name='enroll_list')
    op.alter_column('enroll_list', 'sid',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('enroll_list', 'cid',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('course', sa.Column('student', sa.INTEGER(), nullable=True))
    op.drop_constraint(None, 'course', type_='foreignkey')
    op.drop_index(op.f('ix_course_time2'), table_name='course')
    op.drop_index(op.f('ix_course_time1'), table_name='course')
    op.drop_index(op.f('ix_course_name'), table_name='course')
    op.drop_index(op.f('ix_course_department'), table_name='course')
    op.alter_column('course', 'time2',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('course', 'time1',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('course', 'name',
               existing_type=sa.TEXT(),
               nullable=False)
    op.alter_column('course', 'department',
               existing_type=sa.TEXT(),
               nullable=False)
    op.create_table('sqlite_sequence',
    sa.Column('name', sa.NullType(), nullable=True),
    sa.Column('seq', sa.NullType(), nullable=True)
    )
    # ### end Alembic commands ###
