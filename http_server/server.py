from abc import ABC
from typing import Dict, List

from flask import Flask, request
from flask_cors import CORS

from http_server.exceptions import BaseHttpException
from http_server.adapter import BaseHttpEndpointServiceAdapter


class BaseHttpServer(ABC):
    """
    Abstract classes that other classes can use to register services to an HTTP service and method.
    """
    def __init__(self, port: int = 8080):
        self.app: Flask = Flask(__name__)
        self.services: Dict[str, Dict[str, BaseHttpEndpointServiceAdapter]] = {}
        self.port = port
        self.is_service_routing_setup = False

        CORS(self.app)
    
    def register_services(self, services: List[BaseHttpEndpointServiceAdapter]) -> None:
        """
        Registers services to this server
        :param services: Services to register
        :return: None
        """
        for service in services:
            self.register_service(service)

    def register_service(self, service: BaseHttpEndpointServiceAdapter) -> None:
        """
        Registers a single service to this server
        :param service: Service to register
        :return: None
        """
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

    def handle_request(self) -> Dict | None:
        """
        Handles incoming request
        :return:
        """
        try:
            path = request.path
            method = request.method
            params = request.json if request.is_json else {}
            return self.services[path][method].run(params)
        except BaseHttpException as e:
            return e.dict()
            
    def setup_service_routing(self) -> None:
        """
        Routes every service registered in self into Flask's API routing controller.
        :return: None
        """
        for route in self.services:
            methods = [m for m in self.services[route]]
            self.app.route(route, methods=methods)(self.handle_request)
        self.is_service_routing_setup = True

    def run(self) -> None:
        """
        Runs the server
        :return: None
        """
        if not self.is_service_routing_setup:
            self.setup_service_routing()
        self.app.run(port=self.port)