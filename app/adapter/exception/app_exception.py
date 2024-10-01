"""
Module for the AppError class

:author: Alex Traveylan
:date: 2024
"""


class AppError(Exception):
    """
    Exception class for the application

    Attributes
    ----------
    message : str
        The message of the exception
    """

    def __init__(self, message: str):
        """
        Constructor for AppError

        Parameters
        ----------
        message : str
            The message of the exception
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message
