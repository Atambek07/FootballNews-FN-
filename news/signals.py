"""
Signal handlers for news app.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Team, League


@receiver(post_save, sender=Team)
def create_team_slug(sender, instance, created, **kwargs):
    """
    Create a slug for a team when it's created if it doesn't already have one.
    """
    if created and not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()


@receiver(post_save, sender=League)
def create_league_slug(sender, instance, created, **kwargs):
    """
    Create a slug for a league when it's created if it doesn't already have one.
    """
    if created and not instance.slug:
        instance.slug = slugify(instance.name)
        instance.save()