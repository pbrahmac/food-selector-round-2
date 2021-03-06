"""empty message

Revision ID: 73eaf91f6d93
Revises: 
Create Date: 2019-06-07 23:19:24.293243

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73eaf91f6d93'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('co_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_type', sa.Enum('shaak', 'daal', 'sweet', name='coitemtype'), nullable=True),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_co_items_created'), 'co_items', ['created'], unique=False)
    op.create_index(op.f('ix_co_items_last_modified'), 'co_items', ['last_modified'], unique=False)
    op.create_index(op.f('ix_co_items_name'), 'co_items', ['name'], unique=True)
    op.create_table('food_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item', sa.String(length=128), nullable=True),
    sa.Column('breakfast', sa.Boolean(), nullable=True),
    sa.Column('lunch', sa.Boolean(), nullable=True),
    sa.Column('dinner', sa.Boolean(), nullable=True),
    sa.Column('nutrition', sa.Enum('high', 'medium', 'low', name='nutritionlevel'), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_items_created'), 'food_items', ['created'], unique=False)
    op.create_index(op.f('ix_food_items_item'), 'food_items', ['item'], unique=True)
    op.create_index(op.f('ix_food_items_last_modified'), 'food_items', ['last_modified'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('user_role', sa.Enum('user', 'admin', name='userroles'), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_created'), 'users', ['created'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_firstname'), 'users', ['firstname'], unique=False)
    op.create_index(op.f('ix_users_last_modified'), 'users', ['last_modified'], unique=False)
    op.create_index(op.f('ix_users_lastname'), 'users', ['lastname'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('food_items_co_item_set',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('food_item_id', sa.Integer(), nullable=True),
    sa.Column('co_item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['co_item_id'], ['co_items.id'], ),
    sa.ForeignKeyConstraint(['food_item_id'], ['food_items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_food_items_co_item_set_co_item_id'), 'food_items_co_item_set', ['co_item_id'], unique=False)
    op.create_index(op.f('ix_food_items_co_item_set_food_item_id'), 'food_items_co_item_set', ['food_item_id'], unique=False)
    op.create_table('user_food_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('food_items_id', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('last_modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['food_items_id'], ['food_items.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_food_items_created'), 'user_food_items', ['created'], unique=False)
    op.create_index(op.f('ix_user_food_items_food_items_id'), 'user_food_items', ['food_items_id'], unique=False)
    op.create_index(op.f('ix_user_food_items_last_modified'), 'user_food_items', ['last_modified'], unique=False)
    op.create_index(op.f('ix_user_food_items_user_id'), 'user_food_items', ['user_id'], unique=False)
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_food_items_id', sa.Integer(), nullable=True),
    sa.Column('entry_date', sa.DateTime(), nullable=True),
    sa.Column('meal_time', sa.Enum('breakfast', 'lunch', 'dinner', 'snack', name='mealtimes'), nullable=True),
    sa.ForeignKeyConstraint(['user_food_items_id'], ['user_food_items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_entry_date'), 'schedule', ['entry_date'], unique=True)
    op.create_index(op.f('ix_schedule_user_food_items_id'), 'schedule', ['user_food_items_id'], unique=False)
    op.create_table('schedule_co_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('schedule_id', sa.Integer(), nullable=True),
    sa.Column('food_items_co_item_set_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['food_items_co_item_set_id'], ['food_items_co_item_set.id'], ),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedule_co_items_food_items_co_item_set_id'), 'schedule_co_items', ['food_items_co_item_set_id'], unique=False)
    op.create_index(op.f('ix_schedule_co_items_schedule_id'), 'schedule_co_items', ['schedule_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_schedule_co_items_schedule_id'), table_name='schedule_co_items')
    op.drop_index(op.f('ix_schedule_co_items_food_items_co_item_set_id'), table_name='schedule_co_items')
    op.drop_table('schedule_co_items')
    op.drop_index(op.f('ix_schedule_user_food_items_id'), table_name='schedule')
    op.drop_index(op.f('ix_schedule_entry_date'), table_name='schedule')
    op.drop_table('schedule')
    op.drop_index(op.f('ix_user_food_items_user_id'), table_name='user_food_items')
    op.drop_index(op.f('ix_user_food_items_last_modified'), table_name='user_food_items')
    op.drop_index(op.f('ix_user_food_items_food_items_id'), table_name='user_food_items')
    op.drop_index(op.f('ix_user_food_items_created'), table_name='user_food_items')
    op.drop_table('user_food_items')
    op.drop_index(op.f('ix_food_items_co_item_set_food_item_id'), table_name='food_items_co_item_set')
    op.drop_index(op.f('ix_food_items_co_item_set_co_item_id'), table_name='food_items_co_item_set')
    op.drop_table('food_items_co_item_set')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_lastname'), table_name='users')
    op.drop_index(op.f('ix_users_last_modified'), table_name='users')
    op.drop_index(op.f('ix_users_firstname'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_food_items_last_modified'), table_name='food_items')
    op.drop_index(op.f('ix_food_items_item'), table_name='food_items')
    op.drop_index(op.f('ix_food_items_created'), table_name='food_items')
    op.drop_table('food_items')
    op.drop_index(op.f('ix_co_items_name'), table_name='co_items')
    op.drop_index(op.f('ix_co_items_last_modified'), table_name='co_items')
    op.drop_index(op.f('ix_co_items_created'), table_name='co_items')
    op.drop_table('co_items')
    # ### end Alembic commands ###
