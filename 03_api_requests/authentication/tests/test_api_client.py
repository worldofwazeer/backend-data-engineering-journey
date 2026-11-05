from unittest.mock import Mock, patch

import pytest
import requests

import api_client
from api_client import APIClient


def test_get_returns_json_payload():
    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "application/json"
    }

    expected_payload = {
        "products": [
            {"id": 1, "title": "Phone"},
            {"id": 2, "title": "Laptop"},
        ]
    }

    mock_response.json.return_value = expected_payload

    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.return_value = mock_response

        client = APIClient()

        result = client.get("/products")

        assert result == expected_payload

        mock_session.return_value.get.assert_called_once_with(
            f"{api_client.BASE_URL}/products",
            timeout=api_client.TIMEOUT,
        )

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_called_once_with()


def test_get_raises_http_error():
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("500 Server Error")
    )

    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.return_value = mock_response

        client = APIClient()

        with pytest.raises(
            requests.exceptions.HTTPError,
            match="500 Server Error",
        ):
            client.get("/products")

        mock_response.raise_for_status.assert_called_once_with()
        mock_response.json.assert_not_called()


def test_get_rejects_non_json_response():
    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "text/html"
    }

    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.return_value = mock_response

        client = APIClient()

        with pytest.raises(
            ValueError,
            match="Expected JSON response, got text/html",
        ):
            client.get("/products")

        mock_response.raise_for_status.assert_called_once_with()

        mock_response.json.assert_not_called()


def test_get_raises_for_invalid_json():

    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "application/json"
    }

    mock_response.json.side_effect = (
        ValueError("Invalid JSON payload")
    )
    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.return_value = mock_response

        client = APIClient()

        with pytest.raises(
            ValueError,
        ):
            client.get("/products")


    mock_response.raise_for_status.assert_called_once_with()

    mock_response.json.assert_called_once_with()


def test_get_raises_timeout():
    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.side_effect = (
            requests.exceptions.Timeout("Request timed out")
        )

        client = APIClient()

        with pytest.raises(
            requests.exceptions.Timeout,
            match="Request timed out",
        ):
            client.get("/products")

        mock_session.return_value.get.assert_called_once_with(
            f"{api_client.BASE_URL}/products",
            timeout=api_client.TIMEOUT,
        )

def test_get_raises_connection_error():
    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.side_effect = (
            requests.exceptions.ConnectionError("Connection failed")
        )

        client = APIClient()

        with pytest.raises(
            requests.exceptions.ConnectionError,
            match="Connection failed",
        ):
            client.get("/products")

        mock_session.return_value.get.assert_called_once_with(
            f"{api_client.BASE_URL}/products",
            timeout=api_client.TIMEOUT,
        )


def test_get_forwards_query_parameters():
    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "application/json"
    }

    expected_payload = {
        "products": [
            {"id": 1, "title": "Phone"},
            {"id": 2, "title": "Laptop"},
        ]
    }

    mock_response.json.return_value = expected_payload

    with patch("api_client.requests.Session") as mock_session:
        mock_session.return_value.get.return_value = mock_response

        client = APIClient()

        result = client.get(
                "/products",
                params={"limit": 10, "skip": 0},
            )   

        assert result == expected_payload

        mock_session.return_value.get.assert_called_once_with(
            f"{api_client.BASE_URL}/products",
            timeout=api_client.TIMEOUT,
            params={"limit": 10, "skip": 0}
        )

        mock_response.json.assert_called_once_with()
