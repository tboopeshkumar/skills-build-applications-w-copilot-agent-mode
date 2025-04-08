import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Initialize the database
db = client["octofit_db"]

# Create collections and ensure unique indexes
# Users collection with unique email index
db.users.create_index("email", unique=True)

# Teams collection
db.create_collection("teams")

# Activity collection
db.create_collection("activity")

# Leaderboard collection
db.create_collection("leaderboard")

# Workouts collection
db.create_collection("workouts")

print("Database and collections initialized successfully.")