from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict

from http_server.http_methods import HttpMethods


T = TypeVar('T')


class AbstractHttpServiceAdapter(Generic[T], ABC):
    def __init__(self, route: str, method: HttpMethods, adaptee: T):
        self.method = method
        self.route = route
        self.adaptee = adaptee

    @abstractmethod
    def run(self, params: Dict[str]):
        pass
