class MailupyException(Exception):
    """
    Exception for handling python-related errors.

    It's raised whenever the library encounters an error while preparing the request.
    """
    pass


class MailupyRequestException(MailupyException):
    """
    Exception for handling MailUp errors.

    It's raised whenever the library receive a response with a status code greater than or equal to 400.
    """
    def __init__(self, response):
        super(MailupyException, self).__init__(
            f"Error {response.status_code} - {response.json()}"
        )
