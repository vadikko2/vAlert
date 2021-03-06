"""upload_first_data

Revision ID: 6221cfa708da
Revises: c2f98a9d6db4
Create Date: 2021-04-27 21:05:32.250697

"""
from alembic import op
from json import load

import sys

from sqlalchemy import MetaData, Table

sys.path.append('../')
from vAlert.database.models import CriticalTypesModel, RolesModel

# revision identifiers, used by Alembic.
revision = '6221cfa708da'
down_revision = 'c2f98a9d6db4'
branch_labels = None
depends_on = None


def upgrade():
    meta = MetaData(bind=op.get_bind())
    meta.reflect(only=(CriticalTypesModel.__tablename__, RolesModel.__tablename__))

    critical_types_table = Table(CriticalTypesModel.__tablename__, meta)
    roles_table = Table(RolesModel.__tablename__, meta)
    critical_type_data = load(open('data/critical_types.json'))
    roles_data = load(open('data/roles.json'))

    op.bulk_insert(critical_types_table, critical_type_data)
    op.bulk_insert(roles_table, [dict(name=item) for item in roles_data])


def downgrade():
    pass
