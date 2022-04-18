from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Dict

from http_server.methods import HttpMethod


T = TypeVar('T')


class BaseHttpEndpointServiceAdapter(Generic[T], ABC):
    def __init__(self, route: str, method: HttpMethod, service: T):
        self.method = method
        self.route = route
        self.service = service

    @abstractmethod
    def run(self, params: Dict):
        pass
