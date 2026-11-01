from unittest.mock import Mock, patch

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