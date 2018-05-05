import logging

# This is a minimal configuration to get you started with the Text mode.
# If you want to connect Errbot to chat services, checkout
# the options in the more complete config-template.py from here:
# https://raw.githubusercontent.com/errbotio/errbot/master/errbot/config-template.py
import git
import pathlib
import time

repo = git.Repo('.', search_parent_directories=True)
NOW = time.strftime("%Y%m%d_%H%m%S")
BOT_ROOT = pathlib.PurePath(repo.working_tree_dir, 'bot').as_posix()


BOT_DATA_DIR = f'{BOT_ROOT}/data'
BOT_EXTRA_PLUGIN_DIR = f'{BOT_ROOT}/plugins'

BOT_LOG_FILE = f'{BOT_ROOT}/errbot.log'
BOT_LOG_LEVEL = logging.DEBUG


# Slack
BACKEND = 'Slack'
HOST = '0.0.0.0'
PORT = 9999

BOT_IDENTITY = {
    'token': '',
}

BOT_ADMINS = ('@pyoung',)

CORE_PLUGINS = ()
