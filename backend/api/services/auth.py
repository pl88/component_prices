from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

from backend.config import Settings

PBKDF2_ALGO = "pbkdf2_sha256"
PBKDF2_ITERATIONS = 600_000


def _b64url_encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(f"{data}{padding}")


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return (
        f"{PBKDF2_ALGO}${PBKDF2_ITERATIONS}$"
        f"{base64.b64encode(salt).decode('ascii')}$"
        f"{base64.b64encode(digest).decode('ascii')}"
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algo, iterations_s, salt_s, expected_s = password_hash.split("$", maxsplit=3)
    except ValueError:
        return False

    if algo != PBKDF2_ALGO:
        return False

    try:
        iterations = int(iterations_s)
        salt = base64.b64decode(salt_s)
        expected = base64.b64decode(expected_s)
    except ValueError, binascii.Error:
        return False

    candidate = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(candidate, expected)


def create_access_token(*, user_id: int, email: str, settings: Settings) -> str:
    now = datetime.now(UTC)
    expires_at = now + timedelta(hours=settings.auth_token_ttl_hours)

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int(expires_at.timestamp()),
    }

    header_segment = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_segment = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    signature_segment = _b64url_encode(signature)
    return f"{header_segment}.{payload_segment}.{signature_segment}"


def decode_access_token(token: str, settings: Settings) -> dict[str, Any] | None:
    try:
        header_segment, payload_segment, signature_segment = token.split(".", maxsplit=2)
    except ValueError:
        return None

    signing_input = f"{header_segment}.{payload_segment}".encode("ascii")
    expected_signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    try:
        provided_signature = _b64url_decode(signature_segment)
    except ValueError, binascii.Error:
        return None

    if not hmac.compare_digest(expected_signature, provided_signature):
        return None

    try:
        payload_raw = _b64url_decode(payload_segment)
        payload: dict[str, Any] = json.loads(payload_raw)
    except ValueError, json.JSONDecodeError, binascii.Error:
        return None

    exp = payload.get("exp")
    if not isinstance(exp, int):
        return None
    if exp < int(datetime.now(UTC).timestamp()):
        return None

    return payload
