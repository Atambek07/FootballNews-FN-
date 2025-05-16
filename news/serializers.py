from rest_framework import serializers
from .models import News, Team, League


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'slug', 'league']


class LeagueSerializer(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = ['id', 'name', 'slug']


class NewsSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    leagues = LeagueSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'published_date', 'url', 'source', 'teams', 'leagues']


class NewsListSerializer(serializers.ModelSerializer):
    teams = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    leagues = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = News
        fields = ['id', 'title', 'description', 'published_date', 'url', 'source', 'teams', 'leagues']