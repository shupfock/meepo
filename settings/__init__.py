import os

import toml


config = toml.load(os.path.join(os.path.abspath(__name__), "config.toml"))
try:
    local_config = toml.load(os.path.join(os.path.abspath(__name__), "local_config.toml"))
except FileNotFoundError:
    pass
else:
    config.update(local_config)
