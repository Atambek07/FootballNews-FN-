import logging
import re
import feedparser
from django.utils import timezone
from datetime import datetime
from dateutil import parser as date_parser
from .models import News, Team, League, RSSFeed

logger = logging.getLogger(__name__)

TEAM_KEYWORDS = {
    'Barcelona': ['Barcelona', 'Barca', 'FC Barcelona'],
    'Real Madrid': ['Real Madrid', 'Madrid'],
    'Manchester United': ['Manchester United', 'Man Utd', 'Man United'],
    'Liverpool': ['Liverpool', 'LFC'],
    'Bayern Munich': ['Bayern Munich', 'Bayern', 'FC Bayern'],
    'PSG': ['Paris Saint-Germain', 'PSG', 'Paris SG'],
    'Juventus': ['Juventus', 'Juve'],
    'Chelsea': ['Chelsea', 'CFC'],
    'Manchester City': ['Manchester City', 'Man City'],
    'Arsenal': ['Arsenal', 'AFC'],
}

LEAGUE_KEYWORDS = {
    'Premier League': ['Premier League', 'EPL', 'English Premier League'],
    'La Liga': ['La Liga', 'LaLiga', 'Spanish La Liga'],
    'Bundesliga': ['Bundesliga', 'German Bundesliga'],
    'Serie A': ['Serie A', 'Italian Serie A'],
    'Ligue 1': ['Ligue 1', 'French Ligue 1'],
    'Champions League': ['Champions League', 'UCL', 'UEFA Champions League'],
}


def extract_entities(text):
    """
    Extract team and league mentions from text.
    Returns tuple of (teams, leagues) lists.
    """
    if not text:
        return [], []
    
    found_teams = []
    found_leagues = []
    
    # Look for team mentions
    for team_name, keywords in TEAM_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                found_teams.append(team_name)
                break
    
    # Look for league mentions
    for league_name, keywords in LEAGUE_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text, re.IGNORECASE):
                found_leagues.append(league_name)
                break
    
    return list(set(found_teams)), list(set(found_leagues))


def parse_rss_feeds():
    """
    Parse all active RSS feeds and save news articles.
    """
    logger.info("Starting RSS feed parsing")
    feeds = RSSFeed.objects.filter(is_active=True)
    
    if not feeds.exists():
        logger.warning("No active RSS feeds found")
        return
    
    total_new_articles = 0
    
    for feed in feeds:
        try:
            logger.info(f"Parsing feed: {feed.name}")
            parsed_feed = feedparser.parse(feed.url)
            
            if parsed_feed.bozo and parsed_feed.bozo_exception:
                logger.error(f"Error parsing feed {feed.name}: {parsed_feed.bozo_exception}")
                continue
            
            for entry in parsed_feed.entries:
                # Extract data from feed entry
                title = entry.get('title', '')
                
                # Some feeds use content, others use description or summary
                description = ''
                if hasattr(entry, 'description'):
                    description = entry.description
                elif hasattr(entry, 'summary'):
                    description = entry.summary
                
                link = entry.get('link', '')
                
                # Parse published date
                published_date = timezone.now()
                if hasattr(entry, 'published'):
                    try:
                        published_date = date_parser.parse(entry.published)
                    except:
                        logger.warning(f"Could not parse date: {entry.published}")
                
                # Skip if article already exists
                if News.objects.filter(url=link).exists():
                    continue
                
                # Extract team and league mentions
                combined_text = f"{title} {description}"
                team_names, league_names = extract_entities(combined_text)
                
                # Create news article
                news = News(
                    title=title,
                    description=description,
                    published_date=published_date,
                    url=link,
                    source=feed.name
                )
                news.save()
                
                # Add team relations
                for team_name in team_names:
                    team, created = Team.objects.get_or_create(name=team_name)
                    news.teams.add(team)
                
                # Add league relations
                for league_name in league_names:
                    league, created = League.objects.get_or_create(name=league_name)
                    news.leagues.add(league)
                
                total_new_articles += 1
            
            # Update last fetched timestamp
            feed.mark_fetched()
            
        except Exception as e:
            logger.error(f"Error processing feed {feed.name}: {str(e)}")
    
    logger.info(f"Finished parsing feeds. Added {total_new_articles} new articles.")
    return total_new_articles