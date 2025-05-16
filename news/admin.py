from django.contrib import admin
from .models import News, Team, League, RSSFeed


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_date', 'created_at')
    list_filter = ('source', 'published_date', 'teams', 'leagues')
    search_fields = ('title', 'description')
    date_hierarchy = 'published_date'
    filter_horizontal = ('teams', 'leagues')
    readonly_fields = ('url', 'created_at', 'updated_at')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'league')
    list_filter = ('league',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(RSSFeed)
class RSSFeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active', 'last_fetched')
    list_filter = ('is_active',)
    search_fields = ('name', 'url')