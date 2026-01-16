import requests
import json
from datetime import datetime

API_KEY = "878cab0a56ad8e19e908bd65147e8336"

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

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"data/air_pollution_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved:", filename)
else:
    raise RuntimeError(response.text)
