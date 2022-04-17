from datetime import datetime


class HttpException(BaseException):
    def __init__(self, status: int, error: str, message: str):
        super().__init__()
        self.status = status
        self.error = error
        self.message = message
        self.timestamp = datetime.now().isoformat()

    def dict(self):
        return self.__dict__


class NotAllowedException(HttpException):
    def __init__(self, message: str = 'Method not allowed.'):
        super().__init__(405, 'Not Allowed', message)


class NotFoundException(HttpException):
    def __init__(self, message: str = 'Resource not found.'):
        super().__init__(404, 'Not Found', message)


class BadRequestException(HttpException):
    def __init__(self, message: str = 'An error occurred.'):
        super().__init__(400, 'Bad Request', message)


class InternalServiceException(HttpException):
    def __init__(self, message: str = 'An error occurred.'):
        super().__init__(500, 'Internal Service Error', message)
