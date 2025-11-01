class DataConvertorException(Exception):
    def __init__(self, message, errors=None):
        super().__init__(message)
        self.errors = errors

    def __str__(self):
        if self.errors:
            return f"{self.message} (errors: {self.errors})"
        return self.message
