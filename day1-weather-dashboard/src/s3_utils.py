import boto3
import os
import json
from datetime import datetime

class S3Handler:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.region_name = 'ap-south-1' # Replace with your desired region 
        self.s3 = boto3.client('s3', region_name=self.region_name)

    def create_bucket_if_not_exists(self):
        try:
            self.s3.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    'LocationConstraint': self.region_name 
                }
            )
            print(f"Creating bucket {self.bucket_name}") 
        except Exception as e:
            print(f"Error creating bucket: {e}") 

    def save_weather_data(self, weather_data, city):
        """Save weather data to S3 bucket."""
        if not weather_data:
            return False

        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name = f"weather-data/{city}-{timestamp}.json"

        try:
            weather_data['timestamp'] = timestamp
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved data for {city} to S3")
            return True
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False