def log_init():
    ### Imports
    from logging          import getLogger, DEBUG, INFO, Formatter
    from logging.handlers import RotatingFileHandler
    from os               import sep
    logs = 'log' + sep
    ### Scripts
    logger = getLogger('discord')
    logger.setLevel(DEBUG)
    handler   = RotatingFileHandler(filename = logs + 'discord.log', encoding = 'utf-8', maxBytes = 32 * 1024 * 1024, backupCount = 5)
    formatter = Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', '%Y-%m-%d %H:%M:%S', style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    ### Warnings
    from warnings      import filterwarnings
    # importing warns to ignore
    from scratchattach import LoginDataWarning
    filterwarnings('ignore', category = LoginDataWarning)