import logging
import traceback

from vAlert.config import settings
from vAlert.app import Application

if __name__ == '__main__':
    try:
        with Application() as app:
            app.run()
    except Exception:
        logging.error(f'Сервис {settings.NAME} остановлен: {traceback.format_exc()}')
