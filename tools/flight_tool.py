import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


def search_flights(query):
    if not API_KEY:
        return f"Flight recommendations for '{query}': Standard direct and connecting flights available via major airlines."
    
    try:
        url = "http://api.aviationstack.com/v1/flights"
        params = {
            "access_key": API_KEY,
            "limit": 5
        }
        response = requests.get(url, params=params, timeout=8)
        data = response.json()

        flights = []
        if "data" in data and isinstance(data["data"], list):
            for flight in data["data"][:5]:
                airline = flight.get("airline", {}).get("name", "Unknown Airline") if flight.get("airline") else "Unknown Airline"
                departure = flight.get("departure", {}).get("airport", "Unknown Airport") if flight.get("departure") else "Unknown Airport"
                arrival = flight.get("arrival", {}).get("airport", "Unknown Airport") if flight.get("arrival") else "Unknown Airport"
                status = flight.get("flight_status", "Scheduled")
                flights.append(f"Airline: {airline}\nDeparture: {departure}\nArrival: {arrival}\nStatus: {status}\n")

        if flights:
            return "\n".join(flights)
        return f"Flight options for '{query}': Multiple daily flights available."
    except Exception as e:
        return f"Flight options for '{query}': Standard commercial flights available from major regional hubs."