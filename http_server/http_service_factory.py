from typing import Dict, Type

from http_server import HttpService, HttpMethods


class Service:
    params: Dict
    def run(self): ...


class HttpServiceFactory:
    def create_wrapper_cls(self, route: str, method: HttpMethods, base_service: Type[Service]):
        class _HttpService(HttpService):
            def __init__(self):
                super().__init__(route, method, {})
                self.base_service = base_service()

            def run(self):
                self.base_service.run()
        return _HttpService
