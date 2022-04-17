from abc import ABC, abstractmethod

from commons.http_server.enums import HttpMethods


class HttpService(ABC):
    def __init__(self, route: str, method: HttpMethods):
        self.route = route
        self.method = method

    @abstractmethod
    def run(self):
        pass
