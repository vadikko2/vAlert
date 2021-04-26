import os

from dynaconf import LazySettings

settings = LazySettings(ENVVAR_PREFIX_FOR_DYNACONF=False)

_filepath = os.path.join(os.path.dirname(__file__), '../VERSION')
with open(_filepath, 'r', encoding='utf-8') as f:
    VERSION = f.readline().rstrip()

