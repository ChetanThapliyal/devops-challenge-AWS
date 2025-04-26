# test_s3_utils.py
import unittest
from unittest.mock import patch, MagicMock
from src.s3_utils import S3Handler

class TestS3Handler(unittest.TestCase):
    # ... (your existing setup method)

    @patch('boto3.client') 
    def test_create_bucket_if_not_exists(self, mock_boto3_client):
        """Test bucket creation (mocking S3 client)."""
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Call the function
        self.s3_handler.create_bucket_if_not_exists()

        # Assertions are now against the mock object
        mock_s3.create_bucket.assert_called_once_with(Bucket=self.s3_handler.bucket_name)

    @patch('boto3.client')
    def test_save_weather_data_success(self, mock_boto3_client):
        """Test successful weather data save (mocking S3 client)."""
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        # Test data
        weather_data = {
            'weather': [{'main': 'Sunny'}],
            'temperature': 20
        }
        city = "London"

        # Test 
        result = self.s3_handler.save_weather_data(weather_data, city)

        # Verify
        self.assertTrue(result)  # Assuming your function returns True on success
        mock_s3.put_object.assert_called_once() 
