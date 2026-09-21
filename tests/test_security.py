from datetime import datetime, timedelta, timezone

import jwt
import pytest

from app.core import security
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_hash_password():
    password = "testpassword"
    hashed_password = hash_password(password)

    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_hash_is_salted():
    assert hash_password("testpassword") != hash_password("testpassword")


def test_verify_password_accepts_correct_password():
    hashed_password = hash_password("testpassword")

    assert verify_password("testpassword", hashed_password) is True


def test_verify_password_rejects_wrong_password():
    hashed_password = hash_password("testpassword")

    assert verify_password("testpassword2", hashed_password) is False


def test_token_round_trip():
    token = create_access_token(42)

    payload = decode_access_token(token)

    assert payload["sub"] == "42"
    assert "exp" in payload


def test_expired_token_is_rejected():
    expired = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) - timedelta(minutes=1)},
        security.jwt_secret,
        algorithm=security.jwt_algorithm,
    )

    with pytest.raises(ValueError, match="expired"):
        decode_access_token(expired)


def test_garbage_token_is_rejected():
    with pytest.raises(ValueError, match="Invalid"):
        decode_access_token("not-a-jwt")


def test_token_signed_with_another_key_is_rejected():
    forged = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "some-other-secret-key-that-is-long-enough",
        algorithm=security.jwt_algorithm,
    )

    with pytest.raises(ValueError, match="Invalid"):
        decode_access_token(forged)