from unittest.mock import MagicMock

from botocore.exceptions import ClientError

from src.inventory import (
    InventoryError,
    handle_aws_error,
    main
)


def make_client_error(error_code: str, message: str) -> ClientError:
    """Create a simulated AWS ClientError for testing."""

    return ClientError(
        {
            "Error": {
                "Code": error_code,
                "Message": message,
            }
        },
        "test_operation"
    )


def test_handle_aws_error():
    error = make_client_error(
        "AccessDenied",
        "Access denied"
    )

    result = handle_aws_error(error)

    assert isinstance(result, InventoryError)
    assert str(result) == "AWS permission error (AccessDenied): Access denied"


def test_main_handles_aws_error(monkeypatch):
    def mock_session(*args, **kwargs):
        session = MagicMock()
        sts = session.client.return_value

        sts.get_caller_identity.side_effect = make_client_error(
            "AccessDenied",
            "Access denied"
        )

        return session

    monkeypatch.setattr("src.inventory.boto3.Session", mock_session)

    try:
        main()
    except InventoryError as error:
        assert str(error) == "AWS permission error (AccessDenied): Access denied"
    else:
        raise AssertionError("Expected InventoryError")


def test_handle_aws_unauthorized_operation():
    error = make_client_error(
        "UnauthorizedOperation",
        "Operation is not authorized"
    )

    result = handle_aws_error(error)

    assert isinstance(result, InventoryError)
    assert str(result) == (
        "AWS permission error (UnauthorizedOperation): "
        "Operation is not authorized"
    )

