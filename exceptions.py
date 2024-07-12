class ObjectNotFound(Exception):
    def __init__(self, message="Object with specified id not found"):
        self.message = message
        super().__init__(message)


class ObjectAlreadyExist(Exception):
    def __init__(self, message="Object with specified id already exist"):
        self.message = message
        super().__init__(message)
