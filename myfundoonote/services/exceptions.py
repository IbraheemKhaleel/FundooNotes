class MyExceptions(Exception):
    pass


class EmptyFieldError(MyExceptions):
    def __init__(self, message):
        self.message = message


class LengthError(MyExceptions):
    def __init__(self, message):
        self.message = message


class ValidationError(MyExceptions):
    def __init__(self, message):
        self.message = message


class NoSearchFoundError(MyExceptions):
    def __init__(self, message):
        self.message = message
