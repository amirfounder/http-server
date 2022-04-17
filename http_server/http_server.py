from typing import Dict, Type, Any, Optional

from flask import Flask, request
from flask_cors import CORS

from commons.http_server.enums import HttpMethods
from commons.http_server.exceptions import HttpException, NotAllowedException
from commons.http_server.http_service import HttpService


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

    def register_service(self, service_cls: Type[HttpService], service_params: Optional[Dict[str, Any]] = None):
        service = service_cls(**service_params if service_params else {})
        if service.route in self.services and service.method in self.services[service.route]:
            raise Exception('Service already registered')
        if service.route not in self.services:
            self.services[service.route] = {}
        if service.method not in self.services[service.route]:
            self.services[service.route][service.method] = service

    def run(self):
        for route in self.services:
            controller = HttpController({m.value: s for m, s in self.services[route].items()})
            self.app.route(route, methods=[e.value for e in HttpMethods])(controller.on_request)
        self.app.run(port=self.port)
