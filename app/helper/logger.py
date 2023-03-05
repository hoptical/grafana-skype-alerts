import logging.config

# setup loggers
logging.config.fileConfig('app/logging.conf', disable_existing_loggers=False)

# get root logger
# This will get the root logger since no logger in the configuration has this name.
# the __name__ resolve to "main" since we are at the root of the project.
logger = logging.getLogger(__name__)
