FORMATTERS = {
            'default':
                {
                    'format': '[%(levelname)s] [%(pathname)s %(lineno)d]: %(message)s'
                }
        }

HANDLERS = {
            'stdout':
                {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'stream': 'ext://sys.stdout'
                }
        }

BASE = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers':
        {
            '':
                {
                    'handlers': ['stdout'],
                    'level': 'ERROR',
                }
        }
}

DEBUG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': FORMATTERS,
    'handlers': HANDLERS,
    'loggers':
        {
            '':
                {
                    'handlers': ['stdout'],
                    'level': 'DEBUG',
                }
        }
}
