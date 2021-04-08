from typing import TypeVar, Generic

T = TypeVar("T")


class ModelInstanceNotFound(Generic[T], Exception):
    def __str__(self):
        return f"{self.model_name} is not found"

    @property
    def model_name(self):
        return self.__orig_class__.__args__[0].__name__
