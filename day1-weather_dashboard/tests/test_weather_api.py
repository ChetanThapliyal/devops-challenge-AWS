import unittest
from unittest.mock import patch, Mock
from src.weather_api import WeatherAPI

class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.api_key = "test_api_key"
        self.weather_api = WeatherAPI(self.api_key)

    @patch('requests.get')
    def test_get_weather_data_success(self, mock_get):
        """Test successful weather data retrieval"""
        # Mock response data
        mock_response = Mock()
        mock_response.json.return_value = {
            'weather': [{'main': 'Clear'}],
            'main': {
                'temp': 293.15,  # 20°C
                'temp_min': 291.15,  # 18°C
                'temp_max': 295.15,  # 22°C
                'pressure': 1013,
                'humidity': 60
            },
            'wind': {'speed': 5.1},
            'sys': {
                'sunrise': 1622524800,  # Example timestamp
                'sunset': 1622478000
            }
        }
        mock_get.return_value = mock_response

        # Test
        result = self.weather_api.get_weather_data('London')
        
        # Verify
        self.assertIsNotNone(result)
        self.assertEqual(result['weather'][0]['main'], 'Clear')
        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_weather_data_error(self, mock_get):
        """Test weather data retrieval with error"""
        # Mock error response
        mock_get.side_effect = Exception("API Error")

        # Test
        result = self.weather_api.get_weather_data('NonExistentCity')
        
        # Verify
        self.assertIsNone(result)

    def test_format_weather_display(self):
        """Test weather data formatting"""
        # Test data
        test_data = {
            'weather': [{'main': 'Sunny'}],
            'main': {
                'temp': 293.15,  # 20°C
                'temp_min': 291.15,  # 18°C
                'temp_max': 295.15,  # 22°C
                'pressure': 1013,
                'humidity': 60
            },
            'wind': {'speed': 5.1},
            'sys': {
                'sunrise': 1622524800,
                'sunset': 1622478000
            }
        }

        # Test
        main_info, detailed_info = self.weather_api.format_weather_display(test_data)

        # Verify
        self.assertIn('Sunny', main_info)
        self.assertIn('20°C', main_info)
        self.assertIn('Min Temp: 18°C', detailed_info)
        self.assertIn('Max Temp: 22°C', detailed_info)

if __name__ == '__main__':
    unittest.main()