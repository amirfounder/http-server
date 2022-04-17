from typing import Dict, List

from flask import Flask, request
from flask_cors import CORS

from http_server.http_methods import HttpMethods
from http_server.exceptions import BaseHttpException, NotAllowedException
from http_server.base_http_endpoint_adpater import BaseHttpEndpointAdapter


class HttpServerController:
    def __init__(self, route: str, method_service_map: Dict[str, BaseHttpEndpointAdapter]):
        self.route = route
        self.method_service_map = method_service_map

    def on_request(self):
        try:
            if service := self.method_service_map.get(request.method):
                return service.run(request.json if request.is_json else {})
            raise NotAllowedException()
        except BaseHttpException as e:
            return e.dict()


class BaseHttpServer:
    def __init__(self, port: int = 8080):
        self.app: Flask = Flask(__name__)
        self.services: Dict[str, Dict[str, BaseHttpEndpointAdapter]] = {}
        self.port = port
        self.is_service_routing_setup = False

        CORS(self.app)
    
    def register_services(self, services: List[BaseHttpEndpointAdapter]):
        for service in services:
            self.register_service(service)

    def register_service(self, service: BaseHttpEndpointAdapter):
        route = service.route
        method = service.method.value
        
        is_route_registered = route in self.services
        
        if not is_route_registered:
            self.services[route] = {}
        
        is_method_registered = method in self.services[route]
        
        if not is_method_registered:
            self.services[route][method] = service
            return
        
        raise Exception(f'Service already registered under route, method : {route} {method}')
            
    def setup_service_routing(self):
        for route in self.services:
            route_controller = HttpServerController(route, self.services[route])
            route_methods = [method.value for method in HttpMethods]
            self.app.route(route, methods=route_methods)(route_controller.on_request)
        self.is_service_routing_setup = True

    def run(self):
        if not self.is_service_routing_setup:
            self.setup_service_routing()
        self.app.run(port=self.port)
