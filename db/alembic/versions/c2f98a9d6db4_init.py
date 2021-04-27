"""
Создание исходной структуры базы данных

Revision ID: c2f98a9d6db4
Revises: 
Create Date: 2021-04-26 17:12:43.428716

"""
from alembic import op

import sys

sys.path.append('../')

from vAlert.database.models import (
    ReportsModel,
    CriticalTypesModel,
    RolesModel, SubdivisionsModel,
    PositionsModel, UsersModel, ReportStatusModel
)

revision = 'c2f98a9d6db4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        CriticalTypesModel.__tablename__, *CriticalTypesModel.__schema__
    )
    op.create_table(
        RolesModel.__tablename__, *RolesModel.__schema__
    )

    op.create_table(
        SubdivisionsModel.__tablename__, *SubdivisionsModel.__schema__
    )

    op.create_table(
        PositionsModel.__tablename__, *PositionsModel.__schema__
    )

    op.create_table(
        UsersModel.__tablename__, *UsersModel.__schema__
    )

    op.create_table(
        ReportStatusModel.__tablename__, *ReportStatusModel.__schema__
    )

    op.create_table(ReportsModel.__tablename__, *ReportsModel.__schema__)


def downgrade():
    op.drop_table(ReportsModel.__tablename__)
    op.drop_table(CriticalTypesModel.__tablename__)
    op.drop_table(UsersModel.__tablename__)
    op.drop_table(RolesModel.__tablename__)
    op.drop_table(PositionsModel.__tablename__)
    op.drop_table(SubdivisionsModel.__tablename__)
    op.drop_table(ReportStatusModel.__tablename__)
