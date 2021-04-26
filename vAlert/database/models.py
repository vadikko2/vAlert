from sqlalchemy import Column, Text, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AlembicVersionModel(Base):
    """
    Текущая версия миграции
    """
    __tablename__ = 'alembic_version'
    __table_args__ = {'schema': 'public'}

    version_num = Column('version_num', Text, primary_key=True, doc='Текущая версия миграции')


class ReportModel(Base):
    __tablename__ = 'report'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, doc='Идентификатор')
    title = Column('title', Text, doc='Название')
    creator = Column('creator', Text, doc='Создатель')


class CriticalTypeModel(Base):
    """
    Список типов критичности заявок
    """
    __tablename__ = 'critical_type'
    __table_args__ = {'schema': 'public'}

    id = Column('id', Integer, primary_key=True, doc='Идентификатор')
    name = Column('name', Text, doc='Название')
    probability = Column('probability', Float, doc='Вероятность')
