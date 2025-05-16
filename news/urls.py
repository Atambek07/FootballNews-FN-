from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'news', views.NewsViewSet, basename='news')
router.register(r'teams', views.TeamViewSet)
router.register(r'leagues', views.LeagueViewSet)

urlpatterns = [
    path('', views.api_root),
    path('', include(router.urls)),
]