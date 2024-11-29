import logging
import uuid

class LogConfig:
    # Class-level variables for log format and date format
    LOG_LEVEL = logging.NOTSET
    LOG_FORMAT = '%(asctime)s.%(msecs)03d %(execid)s %(levelname)s %(message)s'
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

    def __init__(self):
        # Generation of an execution ID for debugging and log retrieving
        # Collisions are not a big deal since we can differentiate by timestamp
        self.exec_id = str(uuid.uuid4()).split('-')[0]
        self.old_factory = logging.getLogRecordFactory()

    def record_factory(self, *args, **kwargs):
        """Custom factory to add execution ID to logs"""
        record = self.old_factory(*args, **kwargs)
        record.execid = self.exec_id
        return record

    def setup_logging(self):
        """Set up the logging configuration"""
        logging.basicConfig(
            level=self.LOG_LEVEL,
            format=self.LOG_FORMAT,
            datefmt=self.DATE_FORMAT
        )
        logging.setLogRecordFactory(self.record_factory)
        logging.info("Logging setup completed")