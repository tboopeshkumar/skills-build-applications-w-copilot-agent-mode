from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts
from django.db import connection
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data using raw SQL for efficiency
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM octofit_tracker_user;")
            cursor.execute("DELETE FROM octofit_tracker_team_members;")
            cursor.execute("DELETE FROM octofit_tracker_team;")
            cursor.execute("DELETE FROM octofit_tracker_activity;")
            cursor.execute("DELETE FROM octofit_tracker_leaderboard;")
            cursor.execute("DELETE FROM octofit_tracker_workout;")

        # Populate users
        users = {}
        for user_data in test_users:
            user = User.objects.create(
                email=user_data['email'],
                name=user_data.get('name', user_data['username']),
                age=user_data.get('age', 18),
                username=user_data['username'],
                password=user_data['password']
            )
            users[user.username] = user

        # Populate teams
        for team_data in test_teams:
            team = Team.objects.create(name=team_data['name'])
            team.members.add(*[users[username] for username in team_data['members']])

        # Populate activities
        activity_objects = [
            Activity(
                user=users[activity_data['user']],
                activity_type=activity_data['activity_type'],
                duration=int(timedelta(
                    hours=int(activity_data['duration'].split(':')[0]),
                    minutes=int(activity_data['duration'].split(':')[1])
                ).total_seconds() // 60),
                date=activity_data.get('date', '2025-04-08')
            )
            for activity_data in test_activities
        ]
        Activity.objects.bulk_create(activity_objects)

        # Populate leaderboard
        leaderboard_objects = [
            Leaderboard(
                user=users[leaderboard_data['user']],
                score=leaderboard_data['score']
            )
            for leaderboard_data in test_leaderboard
        ]
        Leaderboard.objects.bulk_create(leaderboard_objects)

        # Populate workouts
        workout_objects = [
            Workout(
                name=workout_data['name'],
                description=workout_data['description'],
                duration=workout_data.get('duration', 60)
            )
            for workout_data in test_workouts
        ]
        Workout.objects.bulk_create(workout_objects)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))