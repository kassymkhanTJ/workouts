from datetime import datetime

from workout_sessions.dao import workout_session_dao
from workout_sessions.models import WorkoutSession, FinishWorkoutSession
from workouts.services import ModelService


class WorkoutSessionService(ModelService[WorkoutSession]):
    def finish_session(self, _id, data: FinishWorkoutSession):
        workout_session = self.get(_id)
        workout_session.state = data.state
        workout_session.finished_at = datetime.now()
        return self.update(_id, workout_session.dict())


workout_session_service = WorkoutSessionService(workout_session_dao)
