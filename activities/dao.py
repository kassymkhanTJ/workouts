from connection import Dao, db
from activities.models import Activity

activity_dao = Dao[Activity](db.workouts, Activity)
