from typing import Type, List, Union, Dict, Any, TypeVar, Generic

import pymongo
from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

from workout_sessions.models import WorkoutSessionState
from workouts.models import Workout, Exercise

client = MongoClient(host="mongodb://mongodb-1-servers-vm-0/workout?replicaSet=rs0")
# test_client = MongoClient(database="test")

db = client.workout

T = TypeVar('T')


class Dao(Generic[T]):
    collection: Collection
    model: Type[BaseModel]

    def __init__(self, collection: Collection, model: Type[BaseModel]):
        self.collection = collection
        self.model = model

    def save(self, obj: BaseModel) -> BaseModel:
        _id = self.collection.insert_one(self._normalize_values(obj.dict())).inserted_id
        return self.get(_id)

    def update(self, _id: str, values: Dict[str, Any]) -> BaseModel:
        self.collection.update_one({"_id": ObjectId(_id)}, {"$set": self._normalize_values(values)})
        return self.get(_id)

    def get(self, _id: str) -> Union[T, None]:
        val = self.collection.find_one({"_id": ObjectId(_id)})
        return val if val is None else self.model(**val)

    def list(self) -> List[BaseModel]:
        return list(map(lambda data: self.model(**data), self.collection.find()))

    def find_one(self, *args, **kwargs):
        data = self.collection.find_one({'state': WorkoutSessionState.START}, sort=[('created_at', pymongo.DESCENDING)])
        return data if data is None else self.model(**data)

    def _normalize_values(self, values: Dict[str, object]) -> Dict[str, object]:
        values = values.copy()
        id = values.pop('_id', None) or values.pop('id', None)
        if id:
            values['_id'] = id
        return values


class WorkoutDao(Dao):
    def list(self) -> List[Workout]:
        query = self.collection.aggregate([
            {'$lookup': {'from': 'exercises',
                         'localField': 'training_sets.rounds.exercise_id',
                         'foreignField': '_id',
                         'as': '_exercises'}}
        ])
        data = list(query)
        self._transform_list(data)
        return list(map(lambda _data: self.model(**_data), data))

    def get(self, _id: str) -> Union[T, None]:
        query = self.collection.aggregate([
            {'$match': {"_id": ObjectId(_id)}},
            {'$lookup': {'from': 'exercises',
                         'localField': 'training_sets.rounds.exercise_id',
                         'foreignField': '_id',
                         'as': '_exercises'}}
        ])
        val = list(query)[0]
        self._transform_obj(val)
        return val if val is None else self.model(**val)

    def _transform_list(self, list_data: List):
        d = dict((e['_id'], e) for w in list_data for e in w['_exercises'])
        for w in list_data:
            self._transform_obj(w, d)

    def _transform_obj(self, w, d=None):
        if not d:
            d = dict((e['_id'], e) for e in w['_exercises'])
        for t in w['training_sets']:
            for r in t['rounds']:
                r['exercise'] = d[r['exercise_id']]
