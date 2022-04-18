from abc import ABC, abstractmethod
from typing import Dict

from http_server import BaseHttpServer, HttpMethod
from http_server.adapter import BaseHttpEndpointServiceAdapter


class BaseService(ABC):
    @abstractmethod
    def perform(self, params: Dict):
        pass


class ConcreteService(BaseService):
    def perform(self, params: Dict):
        return 'Haha'


class ConcreteHttpEndpointServiceAdapter(BaseHttpEndpointServiceAdapter[BaseService]):
    def run(self, params: Dict):
        return self.service.perform(params)


class ConcreteHttpServer(BaseHttpServer):
    def __init__(self):
        super().__init__(port=8081)


SERVICES = [
    ConcreteHttpEndpointServiceAdapter('/', HttpMethod.POST, ConcreteService())
]


if __name__ == '__main__':
    server = ConcreteHttpServer()
    server.register_services(SERVICES)
    server.run()
