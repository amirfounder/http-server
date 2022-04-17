from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict

from http_server.http_methods import HttpMethods


T = TypeVar('T')


class BaseHttpEndpointAdapter(Generic[T], ABC):
    def __init__(self, route: str, method: HttpMethods, service: T):
        self.method = method
        self.route = route
        self.service = service

    @abstractmethod
    def run(self, params: Dict):
        pass
