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
        try : err = response.json()['ErrorDescription']
        except KeyError : err = response.json()['error_description']
        super(MailupyException, self).__init__(
            f"Error {response.status_code} - {err}"
        )
