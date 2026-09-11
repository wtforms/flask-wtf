"""Hardening tests: CSRF raw session token must use secrets, not SHA-1.

Regression coverage for the secrets-module hardening of
``flask_wtf.csrf.generate_csrf``. SHA-1 is deprecated for security
purposes (NIST SP 800-131A, practical collision attacks) and manual
``hashlib.sha1(os.urandom(...))`` truncation is exactly the error-prone
pattern the ``secrets`` module replaces. (Note: itsdangerous itself
still uses SHA-1 internally for HMAC signing -- that is out of scope;
this test targets only the raw-token entropy source in flask_wtf.)
"""

import inspect

from flask import session

import flask_wtf.csrf as csrf_mod
from flask_wtf.csrf import generate_csrf


def test_raw_token_generation_uses_secrets_module(req_ctx, monkeypatch):
    """generate_csrf must source raw-token entropy from secrets.token_hex."""
    calls = []
    real_token_hex = csrf_mod.secrets.token_hex

    def recording_token_hex(nbytes=None):
        calls.append(nbytes)
        return real_token_hex(nbytes) if nbytes is not None else real_token_hex()

    monkeypatch.setattr(csrf_mod.secrets, "token_hex", recording_token_hex)
    # force regeneration so the entropy source is exercised
    session.pop("csrf_token", None)
    token = generate_csrf()
    assert token
    assert calls, "generate_csrf did not use secrets.token_hex for raw token"
    assert calls[0] is not None and calls[0] * 2 >= 64


def test_raw_token_source_has_no_sha1():
    """The raw-token code path must not reference hashlib.sha1."""
    src = inspect.getsource(csrf_mod.generate_csrf)
    assert "sha1" not in src
    assert "os.urandom" not in src


def test_raw_token_has_sufficient_entropy(req_ctx):
    """Raw session token carries at least 256 bits of hex entropy."""
    generate_csrf()
    raw = session["csrf_token"]
    # secrets.token_hex(32) -> 64 lowercase hex chars (256 bits)
    assert isinstance(raw, str)
    assert len(raw) >= 64
    int(raw, 16)  # must be valid hex


def test_raw_tokens_unique_per_session(req_ctx):
    """Two freshly generated raw tokens must differ (no deterministic reuse)."""
    from flask import g

    seen = set()
    for _ in range(20):
        # force regeneration by clearing cached/ stored token
        g.pop("csrf_token", None)
        session.pop("csrf_token", None)
        generate_csrf()
        seen.add(session["csrf_token"])
    assert len(seen) == 20
