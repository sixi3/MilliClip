import json
from pathlib import Path

import pytest

FIX = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class FakeResponse:
    def __init__(self, status=200, body=None, headers=None):
        self.status_code, self._body, self.headers = status, body if body is not None else {}, headers or {}

    def json(self):
        return self._body


class FakeSession:
    """Mocked HTTP layer: pops queued responses (or calls a handler); never touches the network."""

    def __init__(self, responses=None, handler=None):
        self.responses, self.handler, self.calls = list(responses or []), handler, []

    def get(self, url, params=None, headers=None, timeout=None):
        self.calls.append({"url": url, "params": dict(params or {}), "headers": dict(headers or {})})
        if self.handler:
            return self.handler(url, params)
        return self.responses.pop(0)


@pytest.fixture
def fixtures():
    return load
