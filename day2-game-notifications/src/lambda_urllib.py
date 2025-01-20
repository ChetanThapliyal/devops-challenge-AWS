import os
import json
import boto3
from datetime import datetime
import urllib.request
import config
from utils import format_game_data

# Initialize SNS client
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    config_data = config.get_config()
    api_key = config_data['NBA_API_KEY']
    sns_topic_arn = config_data['SNS_TOPIC_ARN']

    try:
        # Get current date in YYYY-MM-DD format (timezone agnostic)
        today_date = datetime.utcnow().strftime('%Y-%m-%d')

        # Construct API URL
        api_url = f"https://api.sportsdata.io/v3/nba/scores/json/GamesByDate/{today_date}?key={api_key}"

        # Make API request using urllib
        with urllib.request.urlopen(api_url) as response:
            if response.status != 200:
                raise Exception(f"Error fetching data: {response.status}")

            # Process game data
            game_data = json.loads(response.read())
            final_games = [game for game in game_data if game['Status'] == 'Final']

            # Format and send notifications for final games
            if final_games:
                messages = [format_game_data(game) for game in final_games]
                publish_to_sns(sns_topic_arn, messages)
            else:
                print("No final games found for today.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def publish_to_sns(sns_topic_arn, messages):
    """Publish messages to SNS topic."""
    message_body = "\n".join(messages)

    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=message_body,
        Subject="NBA Game Scores"
    )

    print(f"Message sent to SNS: {response['MessageId']}")
