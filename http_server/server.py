from abc import ABC
from datetime import datetime
from typing import Dict, List

from flask import Flask, request
from flask_cors import CORS

from http_server.adapter import BaseHttpEndpointServiceAdapter


class BaseHttpServer(ABC):
    """
    Abstract classes that other classes can use to register services to an HTTP service and method.
    """
    def __init__(self, port: int = 8080):
        self.app: Flask = Flask(__name__)
        self.app.config['JSON_SORT_KEYS'] = False
        self.services: Dict[str, Dict[str, BaseHttpEndpointServiceAdapter]] = {}
        self.port = port
        self.is_service_routing_setup = False

        self.config = {'TRUNCATED_LENGTH': 50}

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

        else:
            raise Exception(f'Service already registered under route, method : {route} {method}')

    def handle_request(self) -> Dict | None:
        """
        Handles incoming request
        :return:
        """
        path = request.path
        method = request.method
        params = request.json if request.is_json else {}
        service = self.services[path][method]

        start = datetime.now()

        response_data = self.services[path][method].run(params)

        end = datetime.now()
        elapsed = end - start

        for k, v in params.items():
            if isinstance(v, str) and len(v) > self.config['TRUNCATED_LENGTH']:
                params[k] = v[:self.config['TRUNCATED_LENGTH'] - 3] + '...'

        performance = {
            start: start.isoformat(),
            end: end.isoformat(),
            elapsed: str(elapsed)
        }

        request_data = {
            'path': path,
            'method': method,
            'params': params,
            'service': str(service)
        }

        return {
            'status': 'DONE',
            'request_data': request_data,
            'response_data': response_data,
            'performance': performance
        }

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
