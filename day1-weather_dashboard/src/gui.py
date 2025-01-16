import tkinter as tk

class WeatherGUI:
    def __init__(self, weather_api, s3_handler):
        self.weather_api = weather_api
        self.s3_handler = s3_handler
        self.setup_gui()

    def setup_gui(self):
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Weather App")

        # Font styles
        title_font = ("poppins", 35, "bold")
        detail_font = ("poppins", 15, "bold")

        # Create and pack widgets
        self.search_field = tk.Entry(self.window, justify='center', width=20, font=title_font)
        self.search_field.pack(pady=20)
        self.search_field.focus()
        self.search_field.bind('<Return>', self.get_weather)

        self.main_info_label = tk.Label(self.window, font=title_font)
        self.main_info_label.pack()

        self.detail_info_label = tk.Label(self.window, font=detail_font)
        self.detail_info_label.pack()

    def get_weather(self, event=None):
        city = self.search_field.get()
        weather_data = self.weather_api.get_weather_data(city)
        
        if weather_data:
            main_info, detail_info = self.weather_api.format_weather_display(weather_data)
            self.main_info_label.config(text=main_info)
            self.detail_info_label.config(text=detail_info)
            self.s3_handler.save_weather_data(weather_data, city)

    def run(self):
        self.window.mainloop()