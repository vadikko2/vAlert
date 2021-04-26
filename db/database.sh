#!/bin/bash
CONFIGFILE=config        # Общий кофигурационный файл с переменными
CONFIGPY='vAlert.config' # путь до файла настроек для include питона откуда брать переменные
USE_ALEMBIC=true         # Запускать ли алембик
BACKUP_DB=false

set -a
if [ -d "./venv" ]; then
  source ./venv/bin/activate
fi
if [ -e $CONFIGFILE ]; then source $CONFIGFILE || true; fi
# Присваимваем значения для сервера, имени пользователя, паролю и названию БД из конфига сервиса.
# Из питон конфига проще вытаскивать так.
DB_HOST=$(python3 -c "from ${CONFIGPY} import settings; print(settings.POSTGRES.host)")
DB_PORT=$(python3 -c "from ${CONFIGPY} import settings; print(settings.POSTGRES.port)")
DB_USER=$(python3 -c "from ${CONFIGPY} import settings; print(settings.POSTGRES.user)")
DB_NAME=$(python3 -c "from ${CONFIGPY} import settings; print(settings.POSTGRES.database)")
export PGPASSWORD=$(python3 -c "from ${CONFIGPY} import settings; print(settings.POSTGRES.password)")

# проверяем наличие бд
#export PGPASSWORD='postgres'
DB=$(psql -h ${DB_HOST} -U ${DB_USER} -t -d postgres -c "SELECT datname FROM pg_database WHERE datname='${DB_NAME}'")

# если нет, то создаем новую
if [[ "$DB" ]]; then
  # закрываем все активные сессии бд
  psql -h "${DB_HOST}" -U ${DB_USER} -c "SELECT pg_terminate_backend(pg_stat_activity.pid)
                                            FROM pg_stat_activity
                                            WHERE pg_stat_activity.datname = '${DB_NAME}'
                                            AND pid <> pg_backend_pid();"
fi

# создаем БД
psql -h "${DB_HOST}" -U ${DB_USER} -c "CREATE DATABASE ${DB_NAME};"

# Если для формирования структуры бд используется Алембик
if $USE_ALEMBIC; then
  pushd db
  alembic upgrade head
  popd
fi
