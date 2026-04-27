"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from octofit_tracker import models
from django.http import JsonResponse

# Placeholder serializers and viewsets for demonstration
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Team
        fields = '__all__'

class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leaderboard
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workout
        fields = '__all__'

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = ActivitySerializer

class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = TeamSerializer

class LeaderboardViewSet(viewsets.ModelViewSet):
    queryset = models.Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = models.Workout.objects.all()
    serializer_class = WorkoutSerializer

router = routers.DefaultRouter()
router.register(r'activities', ActivityViewSet, basename='activity')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'leaderboard', LeaderboardViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workout')

def api_root(request):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev/api/"
    else:
        base_url = "http://localhost:8000/api/"
    return JsonResponse({
        'activities': base_url + 'activities/',
        'teams': base_url + 'teams/',
        'leaderboard': base_url + 'leaderboard/',
        'workouts': base_url + 'workouts/',
    })

# Add a simple root view
from django.http import HttpResponse
def home(request):
    return HttpResponse("<h1>Welcome to Octofit Tracker API</h1><p>Visit <a href='/api/'>/api/</a> for API endpoints.</p>")

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
