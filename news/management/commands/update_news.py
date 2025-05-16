import logging
from django.core.management.base import BaseCommand
from news.parsers import parse_rss_feeds
from news.models import RSSFeed

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Update news from RSS feeds'

    def add_arguments(self, parser):
        parser.add_argument(
            '--init',
            action='store_true',
            help='Initialize default RSS feeds if none exist',
        )

    def handle(self, *args, **options):
        if options['init'] and not RSSFeed.objects.exists():
            self.stdout.write('Initializing default RSS feeds...')
            self._init_default_feeds()
        
        self.stdout.write('Fetching news from RSS feeds...')
        count = parse_rss_feeds()
        self.stdout.write(self.style.SUCCESS(f'Successfully added {count} new articles'))

    def _init_default_feeds(self):
        """
        Initialize default RSS feeds if none exist.
        """
        default_feeds = [
            {
                'name': 'BBC Sport Football',
                'url': 'https://feeds.bbci.co.uk/sport/football/rss.xml',
            },
            {
                'name': 'ESPN Soccer',
                'url': 'https://www.espn.com/espn/rss/soccer/news',
            },
            {
                'name': 'Goal.com',
                'url': 'https://www.goal.com/feeds/en/news',
            },
        ]
        
        for feed_data in default_feeds:
            RSSFeed.objects.create(**feed_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(default_feeds)} default RSS feeds'))