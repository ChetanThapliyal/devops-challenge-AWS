import os
from dotenv import load_dotenv
from src.weather_api import WeatherAPI
from src.s3_utils import S3Handler
from src.gui import WeatherGUI

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize components
    api_key = os.getenv('OPENWEATHER_API_KEY')
    bucket_name = os.getenv('AWS_BUCKET_NAME')
    
    weather_api = WeatherAPI(api_key)
    s3_handler = S3Handler(bucket_name)
    
    # Create S3 bucket if it doesn't exist
    s3_handler.create_bucket_if_not_exists()
    
    # Initialize and run GUI
    app = WeatherGUI(weather_api, s3_handler)
    app.run()

if __name__ == "__main__":
    main()