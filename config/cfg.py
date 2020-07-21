
from pathlib import Path

from . import cfgutil

config = {}

config['version'] = '0.0.1'

config['paths'] = {}

config['paths']['root'] = Path('~/archive').expanduser()

config['paths']['sources'] = str(config['paths']['root'].joinpath('sources'))
config['paths']['exp'] = str(config['paths']['root'].joinpath('exp'))
config['paths']['root'] = str(config['paths']['root'])

cfg = cfgutil.get_config_object(config)
