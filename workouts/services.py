from datetime import datetime
from typing import cast, Dict, Any, Generic, TypeVar, List

import pymongo

from exceptions import ModelInstanceNotFound
from workout_sessions.models import WorkoutSessionState
from workouts.dao import workout_dao, exercise_dao
from workouts.models import Workout, Exercise

T = TypeVar('T')


class ModelService(Generic[T]):
    def __init__(self, dao):
        self.dao = dao

    def list(self) -> List[T]:
        return self.dao.list()

    def get(self, _id: str) -> T:
        return self.dao.get(_id)

    def create(self, model_instance: T, additional_fields=None) -> T:
        model_instance.created_at = datetime.now()
        if additional_fields:
            for k, v in additional_fields.items():
                setattr(model_instance, k, v)
        return self.dao.save(model_instance)

    def update(self, _id: str, data: Dict[str, Any]) -> T:
        """
        Be careful, force updates version!!!
        """
        instance = self.dao.get(_id)
        if not instance:
            raise ModelInstanceNotFound[Workout]()
        if hasattr(instance, 'version'):
            data["version"] = instance.version + 1
        data.pop('created_at', None)
        return self.dao.update(_id, data)

    def active(self):
        return self.dao.find_one({'state': WorkoutSessionState.START}, sort=[('created_at', pymongo.DESCENDING)])


workout_service = ModelService[Workout](workout_dao)
exercise_service = ModelService[Exercise](exercise_dao)
