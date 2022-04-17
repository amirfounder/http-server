from abc import ABC, abstractmethod
from typing import Any, Dict

from http_server.http_methods import HttpMethods


class HttpService(ABC):
    def __init__(self, route: str, method: HttpMethods, params: Dict[str, Any]):
        self.route = route
        self.method = method
        self.params = params

    @abstractmethod
    def run(self):
        pass
