import pytest
import requests

import pagination_pipeline


class FakeResponse:
    def __init__(self, payload=None, http_error=None, json_error=None):
        self.payload = payload
        self.http_error = http_error
        self.json_error = json_error

    def raise_for_status(self):
        if self.http_error is not None:
            raise self.http_error

    def json(self):
        if self.json_error is not None:
            raise self.json_error
        return self.payload


class FakeSession:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def get(self, url, *, timeout, params):
        self.calls.append({"url": url, "timeout": timeout, "params": params})
        response = next(self.responses)
        if isinstance(response, BaseException):
            raise response
        return response


def _page(products):
    return FakeResponse(payload={"products": products})


def _use_identity_transforms(monkeypatch):
    monkeypatch.setattr(
        pagination_pipeline, "validate_products", lambda products: products
    )
    monkeypatch.setattr(pagination_pipeline, "transform", lambda products: products)


def _assert_requests(session, skips):
    assert len(session.calls) == len(skips)
    assert [call["params"] for call in session.calls] == [
        {"limit": 20, "skip": skip} for skip in skips
    ]
    assert all(call["timeout"] == 15 for call in session.calls)
    assert all(call["url"] == "https://dummyjson.com/products" for call in session.calls)


def test_nonempty_page_then_empty_page_returns_records_and_stops(monkeypatch):
    _use_identity_transforms(monkeypatch)
    first_page = [{"id": 1}, {"id": 2}]
    session = FakeSession([_page(first_page), _page([])])

    result = pagination_pipeline.fetch_all_products(session)

    assert result == first_page
    _assert_requests(session, [0, 20])


def test_initially_empty_page_returns_empty_result():
    session = FakeSession([_page([])])

    result = pagination_pipeline.fetch_all_products(session)

    assert result == []
    _assert_requests(session, [0])


def test_timeout_after_successful_page_propagates(monkeypatch):
    _use_identity_transforms(monkeypatch)
    timeout = requests.exceptions.Timeout("request timed out")
    session = FakeSession([_page([{"id": 1}]), timeout])

    with pytest.raises(requests.exceptions.Timeout) as exc_info:
        pagination_pipeline.fetch_all_products(session)

    assert exc_info.value is timeout
    _assert_requests(session, [0, 20])


def test_connection_error_propagates():
    connection_error = requests.exceptions.ConnectionError("connection failed")
    session = FakeSession([connection_error])

    with pytest.raises(requests.exceptions.ConnectionError) as exc_info:
        pagination_pipeline.fetch_all_products(session)

    assert exc_info.value is connection_error
    _assert_requests(session, [0])


def test_http_error_propagates():
    http_error = requests.exceptions.HTTPError("server returned an error")
    session = FakeSession([FakeResponse(http_error=http_error)])

    with pytest.raises(requests.exceptions.HTTPError) as exc_info:
        pagination_pipeline.fetch_all_products(session)

    assert exc_info.value is http_error
    _assert_requests(session, [0])


def test_missing_products_field_raises_clear_error():
    session = FakeSession([FakeResponse(payload={})])

    with pytest.raises(ValueError, match="missing 'products' field"):
        pagination_pipeline.fetch_all_products(session)

    _assert_requests(session, [0])


@pytest.mark.parametrize("products", [None, "invalid", {"id": 1}])
def test_non_list_products_value_raises_clear_error(products):
    session = FakeSession([FakeResponse(payload={"products": products})])

    with pytest.raises(ValueError, match="'products' to be a list"):
        pagination_pipeline.fetch_all_products(session)

    _assert_requests(session, [0])


def test_non_object_response_envelope_raises_clear_error():
    session = FakeSession([FakeResponse(payload=[{"id": 1}])])

    with pytest.raises(ValueError, match="expected a JSON object"):
        pagination_pipeline.fetch_all_products(session)

    _assert_requests(session, [0])


def test_invalid_json_error_propagates():
    json_error = requests.exceptions.JSONDecodeError("invalid JSON", "not-json", 0)
    session = FakeSession([FakeResponse(json_error=json_error)])

    with pytest.raises(requests.exceptions.JSONDecodeError) as exc_info:
        pagination_pipeline.fetch_all_products(session)

    assert exc_info.value is json_error
    _assert_requests(session, [0])
