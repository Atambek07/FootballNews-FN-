from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import News, Team, League, RSSFeed
from .parsers import extract_entities
from datetime import datetime
from django.utils import timezone


class NewsModelTests(TestCase):
    def setUp(self):
        self.team1 = Team.objects.create(name='Barcelona', slug='barcelona')
        self.team2 = Team.objects.create(name='Real Madrid', slug='real-madrid')
        self.league = League.objects.create(name='La Liga', slug='la-liga')
        
        self.news = News.objects.create(
            title='Test News',
            description='This is a test news article',
            published_date=timezone.now(),
            url='https://example.com/test-article',
            source='Test Source'
        )
        self.news.teams.add(self.team1, self.team2)
        self.news.leagues.add(self.league)

    def test_news_teams_relation(self):
        self.assertEqual(self.news.teams.count(), 2)
        self.assertIn(self.team1, self.news.teams.all())
        self.assertIn(self.team2, self.news.teams.all())

    def test_news_leagues_relation(self):
        self.assertEqual(self.news.leagues.count(), 1)
        self.assertIn(self.league, self.news.leagues.all())


class NewsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.team1 = Team.objects.create(name='Barcelona', slug='barcelona')
        self.team2 = Team.objects.create(name='Real Madrid', slug='real-madrid')
        self.league = League.objects.create(name='La Liga', slug='la-liga')
        
        self.news1 = News.objects.create(
            title='Barcelona wins',
            description='Barcelona won against Real Madrid',
            published_date=timezone.now(),
            url='https://example.com/article1',
            source='Test Source'
        )
        self.news1.teams.add(self.team1, self.team2)
        self.news1.leagues.add(self.league)
        
        self.news2 = News.objects.create(
            title='Premier League news',
            description='Latest news from Premier League',
            published_date=timezone.now(),
            url='https://example.com/article2',
            source='Test Source'
        )

    def test_get_all_news(self):
        response = self.client.get(reverse('news-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_filter_news_by_team(self):
        response = self.client.get(f"{reverse('news-list')}?teams=Barcelona")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Barcelona wins')

    def test_filter_news_by_league(self):
        response = self.client.get(f"{reverse('news-list')}?leagues=La Liga")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Barcelona wins')


class ParserTests(TestCase):
    def test_extract_entities(self):
        text = "Barcelona and Real Madrid will face off in the next El Clasico of La Liga"
        teams, leagues = extract_entities(text)
        self.assertIn('Barcelona', teams)
        self.assertIn('Real Madrid', teams)
        self.assertIn('La Liga', leagues)

    def test_extract_entities_with_no_match(self):
        text = "No football teams or leagues mentioned here"
        teams, leagues = extract_entities(text)
        self.assertEqual(teams, [])
        self.assertEqual(leagues, [])