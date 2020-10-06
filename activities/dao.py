from connection import Dao, db
from activities.models import Activity

activity_dao = Dao(db.workouts, Activity)
