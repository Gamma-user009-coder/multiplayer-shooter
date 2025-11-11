class InvalidResponseID(Exception):
    def __init__(self, message="Invalid server response provided"):
        super().__init__(message)
        self.value = 0
        self.message = message
    def __str__(self) -> str:
        return self.message


class ServerError(Exception):
    def __init__(self, message="Server misshandled input"):
        super().__init__(message)
        self.value = 1
        self.message = message
    def __str__(self) -> str:
        return self.message

class IllegalAction(Exception):
    def __init__(self, message="Illegal action on client side"):
        super().__init__(message)
        self.value = 2
        self.message = message
    def __str__(self) -> str:
        return self.message
