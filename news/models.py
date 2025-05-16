from django.db import models
from django.utils import timezone


class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    league = models.ForeignKey(League, on_delete=models.SET_NULL, null=True, blank=True, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField(blank=True)
    published_date = models.DateTimeField()
    url = models.URLField(max_length=255, unique=True)
    source = models.CharField(max_length=100)
    teams = models.ManyToManyField(Team, related_name='news', blank=True)
    leagues = models.ManyToManyField(League, related_name='news', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title


class RSSFeed(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    last_fetched = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def mark_fetched(self):
        self.last_fetched = timezone.now()
        self.save()