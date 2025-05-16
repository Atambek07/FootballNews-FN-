import logging
from celery import shared_task
from .parsers import parse_rss_feeds

logger = logging.getLogger(__name__)


@shared_task
def update_news_feeds():
    """
    Celery task to update news from RSS feeds.
    """
    logger.info("Starting scheduled news update task")
    count = parse_rss_feeds()
    logger.info(f"Scheduled news update complete. Added {count} new articles")
    return count