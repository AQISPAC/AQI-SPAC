import os
import json
import requests
from datetime import datetime
from pathlib import Path

# Configuration from GitHub Secrets
API_KEY = os.environ.get('878cab0a56ad8e19e908bd65147e8336')
LATITUDE = os.environ.get('LATITUDE', '6.752670')
LONGITUDE = os.environ.get('LONGITUDE', '125.262184')

# API endpoint
API_URL = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}"

def collect_data():
    """Collect air pollution data from OpenWeather API"""
    try:
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant information
        timestamp = datetime.utcnow().isoformat() + 'Z'
        pollution_data = data['list'][0]
        
        record = {
            'timestamp': timestamp,
            'location': {
                'lat': float(LATITUDE),
                'lon': float(LONGITUDE)
            },
            'aqi': pollution_data['main']['aqi'],
            'components': pollution_data['components'],
            'coord': data['coord']
        }
        
        return record
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing data: {e}")
        return None

def save_data(record):
    """Save collected data to JSON files"""
    if not record:
        print("No data to save")
        return
    
    # Create data directory if it doesn't exist
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    # Save to daily file
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    daily_file = data_dir / f'pollution_{date_str}.json'
    
    # Load existing data or create new list
    if daily_file.exists():
        with open(daily_file, 'r') as f:
            daily_data = json.load(f)
    else:
        daily_data = []
    
    # Append new record
    daily_data.append(record)
    
    # Save updated data
    with open(daily_file, 'w') as f:
        json.dump(daily_data, f, indent=2)
    
    print(f"Data saved to {daily_file}")
    
    # Also save to all-time file
    all_time_file = data_dir / 'all_pollution_data.json'
    
    if all_time_file.exists():
        with open(all_time_file, 'r') as f:
            all_data = json.load(f)
    else:
        all_data = []
    
    all_data.append(record)
    
    with open(all_time_file, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"Data appended to {all_time_file}")
    
    # Create summary statistics
    create_summary(all_data)

def create_summary(all_data):
    """Create summary statistics"""
    if not all_data:
        return
    
    total_records = len(all_data)
    latest_record = all_data[-1]
    
    # Calculate AQI distribution
    aqi_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for record in all_data:
        aqi = record['aqi']
        aqi_counts[aqi] = aqi_counts.get(aqi, 0) + 1
    
    summary = {
        'last_updated': datetime.utcnow().isoformat() + 'Z',
        'total_records': total_records,
        'latest_aqi': latest_record['aqi'],
        'latest_timestamp': latest_record['timestamp'],
        'aqi_distribution': aqi_counts,
        'location': latest_record['location']
    }
    
    summary_file = Path('data') / 'summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Summary updated: {total_records} total records")

def main():
    print("=" * 50)
    print(f"Starting data collection at {datetime.utcnow().isoformat()}Z")
    print(f"Location: ({LATITUDE}, {LONGITUDE})")
    print("=" * 50)
    
    if not API_KEY:
        print("ERROR: OPENWEATHER_API_KEY not set!")
        exit(1)
    
    record = collect_data()
    
    if record:
        print(f"Successfully collected data - AQI: {record['aqi']}")
        save_data(record)
        print("Data collection completed successfully!")
    else:
        print("Failed to collect data")
        exit(1)

if __name__ == "__main__":
    main()
