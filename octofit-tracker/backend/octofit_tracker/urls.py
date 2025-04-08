from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('teams/', views.TeamList.as_view(), name='team-list'),
    path('activity/', views.ActivityList.as_view(), name='activity-list'),
    path('leaderboard/', views.LeaderboardList.as_view(), name='leaderboard-list'),
    path('workouts/', views.WorkoutList.as_view(), name='workout-list'),
]