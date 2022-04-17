from abc import ABC, abstractmethod

from http_server.http_methods import HttpMethods


class HttpService(ABC):
    @abstractmethod
    def __init__(self, route: str, method: HttpMethods):
        self.route = route
        self.method = method

    @abstractmethod
    def run(self):
        pass
