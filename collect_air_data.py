import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("878cab0a56ad8e19e908bd65147e8336")

if not API_KEY:
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

if response.status_code == 200:
    data = response.json()

    # THIS LINE MUST COME BEFORE open()
    os.makedirs("data", exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"data/air_pollution_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved:", filename)
else:
    raise RuntimeError(response.text)
