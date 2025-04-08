from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_data
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Populate users
        users = []
        for user_data in test_data['users']:
            user = User(username=user_data['username'], email=user_data['email'], password=user_data['password'])
            user.save()
            users.append(user)

        # Populate teams
        for team_data in test_data['teams']:
            team = Team(name=team_data['name'])
            team.save()

        # Populate activities
        for activity_data in test_data['activities']:
            user = User.objects.get(username=activity_data['username'])
            duration_minutes = activity_data['duration'].total_seconds() // 60
            activity = Activity(user=user, activity_type=activity_data['activity_type'], duration=duration_minutes)
            activity.save()

        # Populate leaderboard
        for leaderboard_data in test_data['leaderboard']:
            user = User.objects.get(username=leaderboard_data['username'])
            leaderboard = Leaderboard(user=user, score=leaderboard_data['score'])
            leaderboard.save()

        # Populate workouts
        for workout_data in test_data['workouts']:
            workout = Workout(name=workout_data['name'], description=workout_data['description'])
            workout.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))