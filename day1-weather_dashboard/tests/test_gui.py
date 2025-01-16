import unittest
from unittest.mock import Mock, patch
import tkinter as tk
from src.gui import WeatherGUI

class TestWeatherGUI(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.mock_weather_api = Mock()
        self.mock_s3_handler = Mock()
        
        # Create GUI instance
        self.gui = WeatherGUI(self.mock_weather_api, self.mock_s3_handler)

    def tearDown(self):
        """Clean up after tests"""
        try:
            self.gui.window.destroy()
        except:
            pass

    def test_gui_initialization(self):
        """Test GUI initialization"""
        # Verify window title
        self.assertEqual(self.gui.window.title(), "Weather App")
        
        # Verify widgets exist
        self.assertIsInstance(self.gui.search_field, tk.Entry)
        self.assertIsInstance(self.gui.main_info_label, tk.Label)
        self.assertIsInstance(self.gui.detail_info_label, tk.Label)

    def test_get_weather_success(self):
        """Test successful weather data retrieval and display"""
        # Mock weather API response
        self.mock_weather_api.get_weather_data.return_value = {
            'weather': [{'main': 'Sunny'}],
            'temperature': 20
        }
        self.mock_weather_api.format_weather_display.return_value = (
            "Sunny\n20°C",
            "Details about weather"
        )

        # Set city in search field
        self.gui.search_field.insert(0, "London")
        
        # Trigger weather fetch
        self.gui.get_weather()

        # Verify API calls
        self.mock_weather_api.get_weather_data.assert_called_once_with("London")
        self.mock_s3_handler.save_weather_data.assert_called_once()

        # Verify labels were updated
        self.assertEqual(self.gui.main_info_label.cget("text"), "Sunny\n20°C")
        self.assertEqual(self.gui.detail_info_label.cget("text"), "Details about weather")

    def test_get_weather_failure(self):
        """Test weather data retrieval with error"""
        # Mock weather API error response
        self.mock_weather_api.get_weather_data.return_value = None

        # Set city in search field
        self.gui.search_field.insert(0, "NonExistentCity")
        
        # Trigger weather fetch
        self.gui.get_weather()

        # Verify API calls
        self.mock_weather_api.get_weather_data.assert_called_once_with("NonExistentCity")
        self.mock_s3_handler.save_weather_data.assert_not_called()

if __name__ == '__main__':
    unittest.main()