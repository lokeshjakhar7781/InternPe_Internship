import tkinter as tk
from tkinter import messagebox
import requests
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    api_key = "18df00015aa71c1f30cb7b257928d502"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric' 
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            city_name = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            description = data['weather'][0]['description']
            result_text = (
                f"Location: {city_name}, {country}\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Condition: {description.title()}"
            )
            result_label.config(text=result_text)
        elif response.status_code == 404:
            messagebox.showerror("Error", "City not found. Please check the spelling.")
        elif response.status_code == 401:
             messagebox.showerror("Error", "Invalid API Key. Please check your code.")
        else:
            messagebox.showerror("Error", f"Something went wrong.\nStatus code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Could not connect to the API.\n{e}")
root = tk.Tk()
root.title("Real-Time Weather App")
root.geometry("500x500")
root.resizable(False, False)
font_style = ("Helvetica", 12)
header_font = ("Helvetica", 16, "bold")
title_label = tk.Label(root, text="Weather Checker", font=header_font)
title_label.pack(pady=20)
input_frame = tk.Frame(root)
input_frame.pack(pady=10)
city_entry = tk.Entry(input_frame, font=font_style, width=20)
city_entry.pack(side=tk.LEFT, padx=10)
search_btn = tk.Button(input_frame, text="Search", font=font_style, command=get_weather)
search_btn.pack(side=tk.LEFT)
result_label = tk.Label(root, text="", font=("Helvetica", 14), justify=tk.LEFT)
result_label.pack(pady=30)
root.mainloop()