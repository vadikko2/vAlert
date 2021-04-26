"""
Создание исходной структуры базы данных

Revision ID: c2f98a9d6db4
Revises: 
Create Date: 2021-04-26 17:12:43.428716

"""
from alembic import op

from sqlalchemy import Text, Float, Date, ForeignKey, Boolean, Column
from sqlalchemy.dialects.postgresql import UUID

revision = 'c2f98a9d6db4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'critical_types',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('name', Text, comment='Название типа критичности сообщения'),
        Column('frequency', Float, comment='Вероятность выдачи заяки'),
        schema='public', comment='Список типов критичности заявок'
    )

    op.create_table(
        'roles',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('name', Text, unique=True, comment='Название роли'),
        schema='public', comment='Список ролей'
    )

    op.create_table(
        'subdivision',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('name', Text, unique=True, comment='Наименование подразделения'),
        Column('parent_subdivision', UUID(as_uuid=True), ForeignKey('public.subdivision.id'),
               comment='Идентификатор родительского подразделения'),
        schema='public', comment='Список подразделений'
    )

    op.create_table(
        'positions',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('name', Text, unique=True, comment='Наименование позиции'),
        Column('subdivision', UUID(as_uuid=True), ForeignKey('public.subdivision.id'),
               comment='Идентификатор подразделения'),
        Column('parent_position', UUID(as_uuid=True), ForeignKey('public.positions.id'),
               comment='Идентификатор руководителя'),
        schema='public', comment='Список должностей'
    )

    op.create_table(
        'users',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('first_name', Text, comment='Имя'),
        Column('last_name', Text, comment='Фамилия'),
        Column('patronymic', Text, comment='Отчество'),
        Column('email', Text, unique=True, comment='Адрес электронной почты'),
        Column('password_hash', Text, comment='Хэш от пароля'),
        Column('role', UUID(as_uuid=True), ForeignKey('public.roles.id'), comment='Идентификатор роли'),
        Column('disabled', Boolean, comment='Активный пользователь'),
        Column('position', UUID(as_uuid=True), ForeignKey('public.positions.id'), comment='Идентификатор должности'),
        schema='public', comment='Список пользователей'
    )

    op.create_table(
        'report_status',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('name', Text, unique=True, comment='Наименование'),
        schema='public', comment='Список статусов заявки'
    )
    op.create_table(
        'reports',
        Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор'),
        Column('title', Text, comment='Название заявки'),
        Column('description', Text, comment='Описание заявки'),
        Column('timestamp', Date, comment='Времянная метка'),
        Column('reporter', UUID(as_uuid=True), ForeignKey('public.users.id'),
               comment='Идентификатор создателя заявки'),
        Column('critical_types', UUID(as_uuid=True), ForeignKey('public.critical_types.id'), comment='Критичность'),
        Column('resolver', UUID(as_uuid=True), ForeignKey('public.users.id'), comment='Идентификатор эксперта'),
        Column('status', UUID(as_uuid=True), ForeignKey('public.report_status.id'),
               comment='Идентификатор статуса заявки'),
        schema='public', comment='Список заявок'
    )


def downgrade():
    op.drop_table('reports')
    op.drop_table('roles')
    op.drop_table('critical_types')
    op.drop_table('users')
    op.drop_table('subdivision')
    op.drop_table('positions')
    op.drop_table('report_status')
