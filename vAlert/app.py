import asyncio
import logging
import logging.config
import os
from concurrent.futures import ThreadPoolExecutor

from aio_pika import Connection
from fastapi import FastAPI
from uvicorn import run

from broker.deploy import deploy_infra
from broker.utils import get_broker_connection
from vAlert.config import VERSION, settings
import vAlert.api.reports.query as reports
import vAlert.api.users.query as users


class Application:
    def __init__(self):
        self.app = FastAPI()
        self._on_startup = [
            self._init_logging,
            self._init_pool_thread,
            self._init_broker_connection,
            self._deploy_infra

        ]
        self._on_shutdown = [
            self._close_broker_connection
        ]

        self._routes = [
            reports.router,
            users.router
        ]

        self.version = VERSION
        self.app_name = settings.NAME

    def run(self):
        run(app=self.app, host=settings.HOST, port=settings.PORT)

    def _init_pool_thread(self):
        @self.app.on_event('startup')
        async def init():
            self.app.extra['pool_thread'] = ThreadPoolExecutor(max_workers=os.cpu_count())

    def _init_logging(self):
        @self.app.on_event('startup')
        async def init():
            logging.config.dictConfig(settings.LOGGING_BASE_CONFIG)

    def _init_broker_connection(self):
        @self.app.on_event('startup')
        async def connect():
            loop = asyncio.get_event_loop()
            self.app.extra['broker_connection'] = await get_broker_connection(loop)  # type: Connection

    def _close_broker_connection(self):
        @self.app.on_event('shutdown')
        async def connect():
            await self.app.extra['broker_connection'].close()

    def _deploy_infra(self):
        @self.app.on_event('startup')
        async def deploy():
            """
            Разворачивает инфраструктуру внутри раббита (создает все необходимые exchanges/queues/binds).
            Информацию для развертывания берет в constants.py (названия департаментов и приоритеты)
            """
            await deploy_infra(self.app.extra['broker_connection'])

    def startup(self):
        list(map(lambda event: event(), self._on_startup))
        list(map(lambda route: route(), self._routes))

    def shutdown(self):
        list(map(lambda event: event(), self._on_shutdown))

    def __enter__(self):
        self.startup()
        self.run()
        logging.info(f'{self.app_name} запущен: v.{self.version}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
