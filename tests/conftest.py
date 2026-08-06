import socket

import pytest


@pytest.fixture(autouse=True)
def block_network(monkeypatch):
    """Fail every test that attempts an external network connection."""

    def denied(*args, **kwargs):
        raise AssertionError("Network access is forbidden during tests")

    monkeypatch.setattr(socket, "create_connection", denied)
    monkeypatch.setattr(socket.socket, "connect", denied)
