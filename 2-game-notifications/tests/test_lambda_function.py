import os
import json
import pytest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler, format_game_data, publish_to_sns

# Sample environment variables for testing
os.environ['NBA_API_KEY'] = 'test_api_key'
os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789012:test-topic'

@pytest.fixture
def mock_event():
    return {}

@patch('lambda_function.boto3.client')
@patch('lambda_function.requests.get')
def test_lambda_handler(mock_get, mock_boto_client, mock_event):
    # Mocking the SNS client
    mock_sns = MagicMock()
    mock_boto_client.return_value = mock_sns

    # Mocking a successful API response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            'Status': 'Final',
            'AwayTeam': {'Name': 'Team A'},
            'HomeTeam': {'Name': 'Team B'},
            'AwayTeamScore': 100,
            'HomeTeamScore': 98
        }
    ]
    mock_get.return_value = mock_response

    # Call the lambda_handler function
    lambda_handler(mock_event, None)

    # Check that SNS publish was called with the correct message
    expected_message = "Team A vs Team B: 100-98"
    mock_sns.publish.assert_called_once()
    args, kwargs = mock_sns.publish.call_args[0]
    assert expected_message in kwargs['Message']

@patch('lambda_function.requests.get')
def test_lambda_handler_no_games(mock_get, mock_event):
    # Mocking a successful API response with no final games
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    mock_get.return_value = mock_response

    # Call the lambda_handler function
    lambda_handler(mock_event, None)

    # Ensure that no SNS publish is called when there are no games
    with patch('lambda_function.boto3.client') as mock_boto_client:
        mock_boto_client.return_value.publish.assert_not_called()

def test_format_game_data():
    game = {
        'Status': 'Final',
        'AwayTeam': {'Name': 'Team A'},
        'HomeTeam': {'Name': 'Team B'},
        'AwayTeamScore': 100,
        'HomeTeamScore': 98,
    }
    
    result = format_game_data(game)
    expected_result = "Team A vs Team B: 100-98"
    
    assert result == expected_result

def test_format_game_data_in_progress():
    game = {
        'Status': 'InProgress',
        'AwayTeam': {'Name': 'Team A'},
        'HomeTeam': {'Name': 'Team B'},
        'AwayTeamScore': 100,
        'HomeTeamScore': 98,
    }
    
    result = format_game_data(game)
    expected_result = "Team A vs Team B is currently in progress."
    
    assert result == expected_result

def test_format_game_data_no_details():
    game = {
        'Status': 'Scheduled',
        'AwayTeam': {'Name': 'Team A'},
        'HomeTeam': {'Name': 'Team B'},
        'AwayTeamScore': None,
        'HomeTeamScore': None,
    }
    
    result = format_game_data(game)
    
    assert result == "Details are unavailable at this time for this game."

@patch('lambda_function.boto3.client')
def test_publish_to_sns(mock_boto_client):
    # Mocking the SNS client
    sns_client_mock = MagicMock()
    mock_boto_client.return_value = sns_client_mock
    
    messages = ["Game A vs Game B: 100-98", "Game C vs Game D: 95-90"]
    
    publish_to_sns('arn:aws:sns:us-east-1:123456789012:test-topic', messages)
    
    sns_client_mock.publish.assert_called_once()