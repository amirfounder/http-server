from typing import Dict, Type

from flask import Flask, request
from flask_cors import CORS

from http_server.http_methods import HttpMethods
from http_server.exceptions import HttpException, NotAllowedException
from http_server.http_service import HttpService


class HttpController:
    def __init__(self, method_service_map: Dict[HttpMethods, HttpService]):
        self.method_service_map = method_service_map

    def on_request(self):
        try:
            if service := self.method_service_map.get(request.method):
                return service.run()
            raise NotAllowedException()
        except HttpException as e:
            return e.dict()


class HttpServer:
    def __init__(self, port: int = 8080):
        self.app: Flask = Flask(__name__)
        self.services: Dict[str, Dict[HttpMethods, HttpService]] = {}
        self.port = port

        CORS(self.app)

    def register_service(self, service_cls: Type[HttpService], service_params: Dict):
        service = service_cls(service_params)
        if (route := service.route) not in self.services:
            self.services[route] = {}
        if (method := service.method) not in self.services[route]:
            self.services[route][method] = service

    def run(self):
        for route in self.services:
            controller = HttpController({m.value: s for m, s in self.services[route].items()})
            self.app.route(route, methods=[e.value for e in HttpMethods])(controller.on_request)
        self.app.run(port=self.port)
