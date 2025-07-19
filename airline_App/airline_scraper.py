import random
from datetime import datetime, timedelta

def get_airline_data():
    # Simulated data for now; later replace with real scraping or API
    routes = ['Sydney-Melbourne', 'Brisbane-Perth', 'Adelaide-Sydney']
    data = []
    today = datetime.now()

    for i in range(7):
        day = today - timedelta(days=i)
        for route in routes:
            data.append({
                'date': day.strftime('%Y-%m-%d'),
                'route': route,
                'price': random.randint(150, 500),
                'demand': random.randint(100, 300)
            })

    return data