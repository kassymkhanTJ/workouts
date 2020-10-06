from typing import Type, List, Union

from bson import ObjectId
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.collection import Collection

client = MongoClient()

db = client.workout


class Dao:
    collection: Collection
    model: Type[BaseModel]

    def __init__(self, collection: Collection, model: Type[BaseModel]):
        self.collection = collection
        self.model = model

    def save(self, obj: BaseModel) -> BaseModel:
        _id = self.collection.insert_one(obj.dict()).inserted_id
        return self.get(_id)

    def get(self, _id: str) -> Union[BaseModel, None]:
        val = self.collection.find_one({"_id": ObjectId(_id)})
        return val if val is None else self.model(**val)

    def list(self) -> List[BaseModel]:
        return list(map(lambda data: self.model(**data), self.collection.find()))
