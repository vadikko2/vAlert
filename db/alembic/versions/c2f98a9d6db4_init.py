"""
Создание исходной структуры базы данных

Revision ID: c2f98a9d6db4
Revises: 
Create Date: 2021-04-26 17:12:43.428716

"""

from alembic import op

import sys

sys.path.append('../')

from vAlert.database.models import Base

revision = 'c2f98a9d6db4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
