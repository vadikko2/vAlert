import uuid

from sqlalchemy import Column, Text, Float, Date, ForeignKey, Boolean, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CriticalTypesModel(Base):
    """
    Список типов критичности заявок
    """
    __tablename__ = 'critical_types'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Название типа критичности сообщения')
    short_name = Column('short_name', Text, unique=True, comment='Короткое название для служебных нужд')
    frequency = Column('frequency', Float, comment='Вероятность выдачи заяки')


class RolesModel(Base):
    """
    Список ролей
    """
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Название роли')


class SubdivisionsModel(Base):
    """
    Список подразделений
    """
    __tablename__ = 'subdivisions'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Наименование подразделения')
    parent_subdivision = Column('parent_subdivision', Integer,
                                comment='Идентификатор родительского подразделения')


class PositionsModel(Base):
    """
    Список должностей
    """
    __tablename__ = 'positions'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Наименование позиции')
    subdivision = Column('subdivision', Integer, ForeignKey(SubdivisionsModel.id),
                         comment='Идентификатор подразделения')
    parent_position = Column('parent_position', Integer, comment='Идентификатор руководителя')


class UsersModel(Base):
    """
    Список пользователей
    """

    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    first_name = Column('first_name', Text, comment='Имя')
    last_name = Column('last_name', Text, comment='Фамилия')
    patronymic = Column('patronymic', Text, comment='Отчество')
    email = Column('email', Text, unique=True, comment='Адрес электронной почты')
    phone = Column('phone', Text, unique=True, comment='Номер телефона')
    password_hash = Column('password_hash', Text, comment='Хэш от пароля')
    role = Column('role', Integer, ForeignKey(RolesModel.id), comment='Идентификатор роли')
    disabled = Column('disabled', Boolean, comment='Активный пользователь')
    position = Column('position', Integer, ForeignKey(PositionsModel.id),
                      comment='Идентификатор должности')


class ReportStatusModel(Base):
    """
    Список статусов заявки
    """
    __tablename__ = 'report_status'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    name = Column('name', Text, unique=True, comment='Наименование')


class ReportsModel(Base):
    """
    Список заявок
    """
    __tablename__ = 'reports'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, autoincrement=True, comment='Идентификатор')
    title = Column('title', Text, comment='Название заявки')
    description = Column('description', Text, comment='Описание заявки')
    timestamp = Column('timestamp', Date, comment='Времянная метка')
    reporter = Column('reporter', Integer, ForeignKey(UsersModel.id),
                      comment='Идентификатор создателя заявки')
    critical_types = Column('critical_types', Integer, ForeignKey(CriticalTypesModel.id),
                            comment='Критичность')
    resolver = Column('resolver', Integer, ForeignKey(UsersModel.id), comment='Идентификатор эксперта')
    status = Column('status', Integer, ForeignKey(ReportStatusModel.id),
                    comment='Идентификатор статуса заявки')
