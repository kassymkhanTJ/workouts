from datetime import datetime
from typing import cast, Dict, Any, Generic, TypeVar, List

from exceptions import ModelInstanceNotFound
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

    def create(self, model_instance: T) -> T:
        model_instance.created_at = datetime.now()
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


workout_service = ModelService[Workout](workout_dao)
exercise_service = ModelService[Exercise](exercise_dao)
