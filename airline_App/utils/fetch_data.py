import requests
import pandas as pd
from datetime import datetime

def get_airline_data():
    url = "https://opensky-network.org/api/states/all"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        flights = []
        for state in data.get("states", []):
            route = f"{state[2]}"  # origin_country
            price = 100 + hash(state[0]) % 200  # Simulated price
            date = datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d')

            flights.append({
                "route": route,
                "price": price,
                "date": date,
                 "latitude": state[6],  # lat
                 "longitude": state[5]  # lon
            })

        return flights

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def analyze_data(data):
    if not data:
        return {
            "popular_routes": {},
            "average_prices": {},
            "price_trends": {}
        }

    df = pd.DataFrame(data)

    route_counts = df['route'].value_counts().to_dict()
    avg_prices = df.groupby('route')['price'].mean().to_dict()
    date_trends = df.groupby('date')['price'].mean().to_dict()

    return {
        "popular_routes": route_counts,
        "average_prices": avg_prices,
        "price_trends": date_trends
    }
