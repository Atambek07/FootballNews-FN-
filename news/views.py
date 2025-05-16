import logging
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import News, Team, League
from .serializers import NewsSerializer, NewsListSerializer, TeamSerializer, LeagueSerializer

logger = logging.getLogger(__name__)


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows news to be viewed.
    """
    serializer_class = NewsSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['published_date', 'title']
    ordering = ['-published_date']

    def get_queryset(self):
        queryset = News.objects.all()
        
        # Filter by teams if provided
        teams = self.request.query_params.get('teams', None)
        if teams:
            team_names = [name.strip() for name in teams.split(',')]
            queryset = queryset.filter(teams__name__in=team_names).distinct()
        
        # Filter by leagues if provided
        leagues = self.request.query_params.get('leagues', None)
        if leagues:
            league_names = [name.strip() for name in leagues.split(',')]
            queryset = queryset.filter(leagues__name__in=league_names).distinct()
        
        # Filter by source
        source = self.request.query_params.get('source', None)
        if source:
            queryset = queryset.filter(source__iexact=source)

        # Filter by date range
        date_from = self.request.query_params.get('from', None)
        date_to = self.request.query_params.get('to', None)
        
        if date_from:
            queryset = queryset.filter(published_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(published_date__lte=date_to)

        # Filter by time period
        period = self.request.query_params.get('period', None)
        if period:
            now = timezone.now()
            if period == 'today':
                queryset = queryset.filter(published_date__date=now.date())
            elif period == 'week':
                queryset = queryset.filter(published_date__gte=now - timedelta(days=7))
            elif period == 'month':
                queryset = queryset.filter(published_date__gte=now - timedelta(days=30))
        
        # Search term
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search)
            ).distinct()
            
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return NewsListSerializer
        return NewsSerializer

    @action(detail=False, methods=['get'])
    def latest(self):
        """
        Get the latest news articles (last 24 hours).
        """
        latest_news = self.get_queryset().filter(
            published_date__gte=timezone.now() - timedelta(days=1)
        )
        serializer = self.get_serializer(latest_news, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sources(self):
        """
        Get list of all news sources.
        """
        sources = News.objects.values_list('source', flat=True).distinct()
        return Response({'sources': list(sources)})


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows teams to be viewed.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'league__name']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def news(self, request, pk=None):
        """
        Get all news for a specific team.
        """
        team = self.get_object()
        news = team.news.all().order_by('-published_date')
        serializer = NewsListSerializer(news, many=True)
        return Response(serializer.data)


class LeagueViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows leagues to be viewed.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def teams(self, request, pk=None):
        """
        Get all teams in a specific league.
        """
        league = self.get_object()
        teams = league.teams.all().order_by('name')
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def news(self, request, pk=None):
        """
        Get all news for a specific league.
        """
        league = self.get_object()
        news = league.news.all().order_by('-published_date')
        serializer = NewsListSerializer(news, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def api_root(request):
    """
    API root showing available endpoints.
    """
    return Response({
        'news': {
            'list': request.build_absolute_uri('/api/news/'),
            'latest': request.build_absolute_uri('/api/news/latest/'),
            'sources': request.build_absolute_uri('/api/news/sources/'),
        },
        'teams': request.build_absolute_uri('/api/teams/'),
        'leagues': request.build_absolute_uri('/api/leagues/'),
    })