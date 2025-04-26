import os

def get_config():
    """Retrieve configuration settings from environment variables."""
    config = {
        'NBA_API_KEY': os.getenv('NBA_API_KEY'),
        'SNS_TOPIC_ARN': os.getenv('SNS_TOPIC_ARN')
    }
    
    if not all(config.values()):
        raise ValueError("Missing required environment variables. Please check your configuration.")
    return config