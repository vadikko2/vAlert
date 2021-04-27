from sqlalchemy import Column, Text, Float, Date, ForeignKey, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ExtendTable(Table):
    def __new__(cls, metadata):
        self = super().__new__(cls, cls.__tablename__, metadata,
                               *cls.__schema__)
        return self


class AlembicVersionModel(ExtendTable):
    """
    Текущая версия миграции
    """
    __tablename__ = 'alembic_version'
    __table_args__ = {'schema': 'public'}

    version_num = Column('version_num', Text, primary_key=True, doc='Текущая версия миграции')

    __schema__ = [version_num]


class CriticalTypesModel(ExtendTable):
    """
    Список типов критичности заявок
    """
    __tablename__ = 'critical_types'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Название типа критичности сообщения')
    short_name = Column('short_name', Text, unique=True, comment='Короткое название для служебных нужд')
    frequency = Column('frequency', Float, comment='Вероятность выдачи заяки')

    __schema__ = [
        id, name, short_name, frequency
    ]


class RolesModel(ExtendTable):
    """
    Список ролей
    """
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Название роли')

    __schema__ = [
        id, name
    ]


class SubdivisionsModel(ExtendTable):
    """
    Список подразделений
    """
    __tablename__ = 'subdivisions'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Наименование подразделения')
    parent_subdivision = Column('parent_subdivision', UUID(as_uuid=True),
                                comment='Идентификатор родительского подразделения')

    __schema__ = [
        id, name, parent_subdivision
    ]


class PositionsModel(ExtendTable):
    """
    Список должностей
    """
    __tablename__ = 'positions'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Наименование позиции')
    subdivision = Column('subdivision', UUID(as_uuid=True), ForeignKey(SubdivisionsModel.id),
                         comment='Идентификатор подразделения')
    parent_position = Column('parent_position', UUID(as_uuid=True), comment='Идентификатор руководителя')
    __schema__ = [
        id, name, subdivision, parent_position
    ]


class UsersModel(ExtendTable):
    """
    Список пользователей
    """

    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    first_name = Column('first_name', Text, comment='Имя')
    last_name = Column('last_name', Text, comment='Фамилия')
    patronymic = Column('patronymic', Text, comment='Отчество')
    email = Column('email', Text, unique=True, comment='Адрес электронной почты')
    phone = Column('phone', Text, unique=True, comment='Номер телефона')
    password_hash = Column('password_hash', Text, comment='Хэш от пароля')
    role = Column('role', UUID(as_uuid=True), ForeignKey(RolesModel.id), comment='Идентификатор роли')
    disabled = Column('disabled', Boolean, comment='Активный пользователь')
    position = Column('position', UUID(as_uuid=True), ForeignKey(PositionsModel.id),
                      comment='Идентификатор должности')

    __schema__ = [
        id, first_name, last_name,
        patronymic, email, phone,
        password_hash, role, disabled,
        position
    ]


class ReportStatusModel(ExtendTable):
    """
    Список статусов заявки
    """
    __tablename__ = 'report_status'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Наименование')

    __schema__ = [
        id, name
    ]


class ReportsModel(ExtendTable):
    """
    Список заявок
    """
    __tablename__ = 'reports'
    __table_args__ = {'schema': 'public'}

    id = Column('id', UUID(as_uuid=True), primary_key=True, comment='Идентификатор')
    title = Column('title', Text, comment='Название заявки')
    description = Column('description', Text, comment='Описание заявки')
    timestamp = Column('timestamp', Date, comment='Времянная метка')
    reporter = Column('reporter', UUID(as_uuid=True), ForeignKey(UsersModel.id),
                      comment='Идентификатор создателя заявки')
    critical_types = Column('critical_types', UUID(as_uuid=True), ForeignKey(CriticalTypesModel.id),
                            comment='Критичность')
    resolver = Column('resolver', UUID(as_uuid=True), ForeignKey(UsersModel.id), comment='Идентификатор эксперта')
    status = Column('status', UUID(as_uuid=True), ForeignKey(ReportStatusModel.id),
                    comment='Идентификатор статуса заявки')

    __schema__ = [
        id, title, description, title, timestamp,
        reporter, critical_types, resolver, status
    ]
