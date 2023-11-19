import logging
import logging.config

from lucky_number.core import settings, security


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.args and len(record.args) >= 3:
            return not record.args[2].startswith(('/health', '/log'))
        return False


class FilterNoQuotes(logging.Filter):
    def filter(self, record):
        if isinstance(record.msg, str):
            record.msg = record.msg.replace('"', '')
        return record


class RedactingFilter(logging.Filter):

    def __init__(self, patterns):
        super(RedactingFilter, self).__init__()
        self._patterns = patterns

    def filter(self, record):
        record.args = tuple(self.redact(arg) for arg in record.args)
        return record

    def redact(self, msg):
        if not msg or not isinstance(msg, str):
            return msg
        for pattern in self._patterns:
            msg = msg.replace(pattern, "***")
        return msg


def setup_logging():
    logging_level = settings.get("LOGGING_LEVEL", "DEBUG")
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s - %(levelname)-8s - %(name)-25s - %(message)s')
            },
            'gcp': {
                'format': ('{"severity":"%(levelname)s","time":"%(asctime)s","caller":"%(name)s","message":"%(message)s"}'),
                'datefmt': '%Y-%m-%dT%H:%M:%S%z'
            },
        },
        'handlers': {
            'console': {
                'level': logging_level,
                'class': 'logging.StreamHandler',
                'formatter': 'gcp'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename':  settings.get("LOGGING_FILE_NAME"),
                'maxBytes': 1024 * 1024 * 1000,  # 1 GB,
                'backupCount': 3,
                'formatter': 'gcp',
            },
        },
        'loggers': {
            'lucky_number': {
                'level': logging_level,
                'handlers': ['console', 'file'],
            }
        }
    }

    # use defaul config
    logging.config.dictConfig(logging_config)

    # add filter to the logger
    logging.getLogger("uvicorn.access").addFilter(EndpointFilter())
    logging.getLogger("uvicorn.access").addFilter(
        RedactingFilter(security.get_api_keys()))
    logging.getLogger("uvicorn.access").addFilter(FilterNoQuotes())
