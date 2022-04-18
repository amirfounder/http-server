from abc import ABC, abstractmethod
from typing import Dict

from http_server import BaseHttpServer, HttpMethod
from http_server.adapter import BaseHttpEndpointServiceAdapter


class BaseService(ABC):
    @abstractmethod
    def perform(self, params: Dict):
        pass


class Service(BaseService):
    def perform(self, params: Dict):
        return 'Haha'


class HttpEndpointServiceAdapter(BaseHttpEndpointServiceAdapter[BaseService]):
    def run(self, params: Dict):
        return self.service.perform(params)


class HttpServer(BaseHttpServer):
    def __init__(self):
        super().__init__(port=8081)


SERVICES = [
    HttpEndpointServiceAdapter('/', HttpMethod.POST, Service())
]


if __name__ == '__main__':
    server = HttpServer()
    server.register_services(SERVICES)
    server.run()
