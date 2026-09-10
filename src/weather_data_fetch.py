"""
Leipzig Weather & Air Quality Data Fetch
-----------------------------------------
Fetches 7-day hourly weather forecast and air quality data
for Leipzig from the Open-Meteo API (free, keyless).

Used inside Power Query (Power BI) or standalone.

Author: Danush Kumar Sekar
License: MIT
"""

import requests
import pandas as pd


def fetch_leipzig_weather(days: int = 7) -> pd.DataFrame:
    """
    Fetches hourly weather + air quality data for Leipzig.

    Args:
        days: Number of forecast days (Open-Meteo supports 1-16).

    Returns:
        pandas.DataFrame with hourly weather metrics.
    """
    lat, lon = 51.3397, 12.3731  # Leipzig coordinates

    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,apparent_temperature,relative_humidity_2m,"
        f"precipitation,precipitation_probability,wind_speed_10m,cloud_cover,weather_code"
        f"&forecast_days={days}"
        f"&timezone=Europe/Berlin"
    )

    aqi_url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={lat}&longitude={lon}"
        f"&hourly=pm10,pm2_5,us_aqi,european_aqi"
        f"&forecast_days={days}"
        f"&timezone=Europe/Berlin"
    )

    forecast_data = requests.get(forecast_url).json()['hourly']
    aqi_data = requests.get(aqi_url).json()['hourly']

    hourly = []
    for i, ts in enumerate(forecast_data['time']):
        hourly.append({
            'DateTime': ts,
            'Temperature (°C)': forecast_data['temperature_2m'][i],
            'Feels Like (°C)': forecast_data['apparent_temperature'][i],
            'Humidity (%)': forecast_data['relative_humidity_2m'][i],
            'Precipitation (mm)': forecast_data['precipitation'][i],
            'Chance of Rain (%)': forecast_data['precipitation_probability'][i],
            'Wind Speed (km/h)': forecast_data['wind_speed_10m'][i],
            'Cloud Cover (%)': forecast_data['cloud_cover'][i],
            'Weather Code': forecast_data['weather_code'][i],
            'PM2.5 (Fine Particulates)': aqi_data['pm2_5'][i] if i < len(aqi_data['time']) else None,
            'PM10 (Particulates)': aqi_data['pm10'][i] if i < len(aqi_data['time']) else None,
            'US EPA Index': aqi_data['us_aqi'][i] if i < len(aqi_data['time']) else None,
            'European AQI': aqi_data['european_aqi'][i] if i < len(aqi_data['time']) else None,
        })

    df = pd.DataFrame(hourly)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df


if __name__ == "__main__":
    df = fetch_leipzig_weather(days=7)
    print(f"Fetched {len(df)} hourly records for Leipzig")
    print(df.head())
    df.to_csv("leipzig_weather_sample.csv", index=False)
    print("Sample saved to leipzig_weather_sample.csv")
