class MLServiceException(Exception):
    pass


class InsufficientBalanceException(MLServiceException):
    pass


class PredictionFailedException(MLServiceException):
    pass


class MLTaskFailedException(MLServiceException):
    pass
