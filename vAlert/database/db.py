import databases
import sqlalchemy

from vAlert.config import settings


class Database:

    def __init__(self):
        self._url = f'postgresql://{settings.POSTGRES.user}:{settings.POSTGRES.password}@{settings.POSTGRES.password}' \
                    f'/{settings.POSTGRES.database}'
        self.database = databases.Database(self._url)
        self._metadata = sqlalchemy.MetaData()
        self._engine = sqlalchemy.create_engine(self._url)
        self._metadata.create_all(self._engine)

    async def connect(self):
        await self.database.connect()

    async def disconnect(self):
        await self.database.disconnect()
