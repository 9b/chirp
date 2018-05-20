"""Tasks related to celery."""
from .. import mongo, logger
import celery


@celery.task(name="heartbeat")
def heartbeat():
    """Look alive."""
    logger.debug("I am the beat.")
