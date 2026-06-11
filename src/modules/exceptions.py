class InvalidCredentials(Exception):
    def __init__(self, message="Invalid credentials."):
        super().__init__(message)

class UserAlreadyExists(InvalidCredentials):
    def __init__(self, message="User already exists."):
        super().__init__(message)

class UserDoesNotExist(InvalidCredentials):
    def __init__(self, message="User does not exist."):
        super().__init__(message)

class InvalidPassword(InvalidCredentials):
    def __init__(self, message="Invalid password."):
        super().__init__(message)

