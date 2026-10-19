from unittest.mock import Mock, patch
import requests
import pytest

from dvsa_client import DVSA_API_Client

@patch("dvsa_client.requests.get")
def test_get_mot_history_success(mock_get):
    fake_response = Mock()
    fake_response.json.return_value = {'abc':123}
    mock_get.return_value = fake_response

    client = DVSA_API_Client(5,'123','test')
    output = client.get_mot_history('J557KAE')
    assert output == {'abc':123}

@patch("dvsa_client.requests.get")
def test_404_return(mock_get):
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found!")
    mock_get.return_value = fake_response

    client = DVSA_API_Client(5, "123", "test")

    with pytest.raises(requests.HTTPError):
        client.get_mot_history("J557KAE")

@patch("dvsa_client.requests.get")
def test_timeout(mock_get):
    mock_get.side_effect = requests.Timeout("Request timed out")

    client = DVSA_API_Client(5, "123", "test")

    with pytest.raises(requests.Timeout):
        client.get_mot_history("J557KAE")

@patch("dvsa_client.requests.get")
def test_timeout_retry(mock_get):
    fake_response = Mock()
    fake_response.json.return_value = {'J557KAE':'test'}
    mock_get.side_effect = [
        requests.Timeout(),
        requests.Timeout(),
        fake_response
    ]

    client = DVSA_API_Client(5, "123", "test")
    output = client.get_mot_history('J557KAE')
    assert output == {'J557KAE':'test'}
    assert mock_get.call_count == 3


