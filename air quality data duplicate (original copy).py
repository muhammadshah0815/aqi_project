import requests
import json
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

#TODO: fix graphs

API_KEY = "aae333df-e2c1-4629-812b-bc2749923aa4"
DATABASE_NAME = "aqi_data.db"
TABLE_NAME = "aqi_records"

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} (timestamp TEXT, aqi INTEGER)")
    conn.commit()
    conn.close()

def store_aqi_data(city, aqi):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(f"INSERT INTO {TABLE_NAME} (timestamp, aqi) VALUES (?, ?)", (timestamp, aqi))
    conn.commit()
    conn.close()

def retrieve_aqi_data():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute(f"SELECT timestamp, aqi FROM {TABLE_NAME}")
    data = c.fetchall()
    conn.close()
    return data

def get_air_quality_data(city):
    # ERROR: State is set to Punjab, so only that one state included
    url = f"https://api.airvisual.com/v2/city?city={city}&state=Punjab&country=Pakistan&key={API_KEY}"
    response = requests.get(url)
    data = json.loads(response.text)

    if data["status"] == "success":
        aqi = data["data"]["current"]["pollution"]["aqius"]
        print(f"AQI in {city}: {aqi}")
        store_aqi_data(city, aqi)  # Store the AQI data in the database
        return aqi
    else:
        print("Unable to retrieve air quality data.")
        return None

def plot_aqi_chart(city, data):
    timestamps = [row[0] for row in data]
    aqi_values = [row[1] for row in data]
    plt.figure(figsize=(20, 6))
    plt.title(f"AQI in {city}")
    plt.xlabel("Time")
    plt.ylabel("AQI")
    plt.plot(timestamps, aqi_values)  # Plot the AQI values over time
    plt.xticks(rotation=45) # stil giving errors
    plt.show()

def main():
    city = input("Enter the name of a city in Pakistan: ")
    create_database()  # Create the database if it doesn't exist
    aqi = get_air_quality_data(city)
    if aqi is not None:
        data = retrieve_aqi_data()  # Retrieve all AQI data from the database
        plot_aqi_chart(city, data)  # Plot the AQI data

if __name__ == "__main__":
    main()
