"""
Test the AppException class

:author: Alex Traveylan
:date: 2024
"""

from app.adapter.exception.app_exception import AppError


def test_app_exception():
    """Test the AppException class."""

    message = "Test exception message"
    exception = AppError(message)

    assert str(exception) == message
