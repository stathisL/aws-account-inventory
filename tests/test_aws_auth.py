from unittest.mock import MagicMock

from src.aws_auth import assume_role


def test_assume_role():
    source_session = MagicMock()
    sts = source_session.client.return_value

    sts.assume_role.return_value = {
        "Credentials": {
            "AccessKeyId": "temporary-access-key",
            "SecretAccessKey": "temporary-secret-key",
            "SessionToken": "temporary-session-token"
        }
    }

    result = assume_role(
        session=source_session,
        account_id="191919191919",
        role_name="AWSInventoryReadOnly"
    )

    source_session.client.assert_called_once_with("sts")

    sts.assume_role.assert_called_once_with(
        RoleArn="arn:aws:iam::191919191919:role/AWSInventoryReadOnly",
        RoleSessionName="aws-account-inventory"
    )

    assert result is not None
