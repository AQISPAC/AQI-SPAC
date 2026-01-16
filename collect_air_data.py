import requests
import json
import os
from datetime import datetime

# READ API KEY (THIS WORKS – WE KNOW IT EXISTS)
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

# SAFETY CHECK
if API_KEY is None or API_KEY.strip() == "":
    raise RuntimeError("OPENWEATHER_API_KEY not found")

LAT = 6.752670
LON = 125.262184

url = "http://api.openweathermap.org/data/2.5/air_pollution"

params = {
    "lat": LAT,
    "lon": LON,
    "appid": API_KEY
}

response = requests.get(url, params=params)

if response.status_code != 200:
    raise RuntimeError(response.text)

data = response.json()

# ENSURE DATA DIRECTORY EXISTS
os.makedirs("data", exist_ok=True)

timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
filename = f"data/air_pollution_{timestamp}.json"

with open(filename, "w") as f:
    json.dump(data, f, indent=4)

print("Saved:", filename)
