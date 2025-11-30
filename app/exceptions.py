class UnhandledException(Exception):
    def __init__(self, msg: str):
        message = f'Sorry, the request failed with error: {msg}'
        super().__init__(message)


class UnauthorizedException(Exception):
    def __init__(self):
        message = 'API key is invalid'
        super().__init__(message)


class InvalidCityException(Exception):
    def __init__(self, city: str):
        message = f'Invalid input: {city}'
        super().__init__(message)
