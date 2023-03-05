from dotenv import load_dotenv
from fastapi.testclient import TestClient
from unittest.mock import patch
import json
from app.main import app, get_skype
from app.helper.skype_utils import SkypeUtils
import json
import pytest

load_dotenv("tests/test.env", override=True)


def override_get_skype():
    skype_instance = SkypeUtils(connect=False)
    yield skype_instance


app.dependency_overrides[get_skype] = override_get_skype

client = TestClient(app)

# Opening JSON file
with open('tests/sample.json') as f:
    sample_alert = json.load(f)


@patch('app.main.SkypeUtils.translate_room_name')
def test_room_name_to_chat_id(mock_translate):
    # Mock the send_message method of the skype_instance object to do nothing
    dummy_value = "skype@e3rwerwer"
    mock_translate.return_value = dummy_value
    # Make a POST request to the notify endpoint with a mock chat ID and the fake alert object

    response = client.get('/api/skype/grafana_alert/123')
    # Assert that the response has a 200 status code and the expected message
    assert response.status_code == 200
    assert response.json() == dummy_value


@patch('app.main.SkypeUtils.send_message')
@pytest.mark.parametrize("test_input", sample_alert)
def test_notify(mock_send_message, test_input):
    # Mock the send_message method of the skype_instance object to do nothing
    mock_send_message.return_value = None
    # Make a POST request to the notify endpoint with a mock chat ID and the fake alert object

    response = client.post('/api/skype/grafana_alert/123', json=test_input)
    # Assert that the response has a 200 status code and the expected message
    assert response.status_code == 200
    assert response.json() == "Grafana alert sent to the channel"
    # Assert that the send_message method of the skype_instance object was called with the expected arguments
    #mock_send_message.assert_called_once_with('123', alert.model_representer(verbose=False))
