import requests

OPENSKY_URL = "https://opensky-network.org/api/states/all"

# Index positions in the OpenSky state vector list
ICAO24 = 0
CALLSIGN = 1
ORIGIN_COUNTRY = 2
LONGITUDE = 5
LATITUDE = 6
GEO_ALTITUDE = 13
VELOCITY = 9


def fetch_live_flights(bbox=None):
    """
    Fetch live aircraft state vectors from the OpenSky Network API.

    bbox: optional tuple (min_lat, max_lat, min_lon, max_lon) to limit results
          to a geographic bounding box. If None, fetches all aircraft worldwide.

    Returns the raw JSON dict from the API, or None if the request fails.
    """
    params = {}
    if bbox is not None:
        min_lat, max_lat, min_lon, max_lon = bbox
        params = {
            "lamin": min_lat,
            "lamax": max_lat,
            "lomin": min_lon,
            "lomax": max_lon,
        }

    try:
        response = requests.get(OPENSKY_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def parse_flight_data(raw_data):
    """
    Parse raw OpenSky JSON into a clean list of flight dicts.

    Skips any aircraft where latitude or longitude is None.

    Returns a list of dicts with keys:
        callsign, origin_country, longitude, latitude, altitude, velocity
    """
    if not raw_data or "states" not in raw_data or raw_data["states"] is None:
        return []

    flights = []
    for state in raw_data["states"]:
        lat = state[LATITUDE]
        lon = state[LONGITUDE]

        if lat is None or lon is None:
            continue

        callsign = (state[CALLSIGN] or "").strip() or "N/A"
        altitude = state[GEO_ALTITUDE]
        velocity = state[VELOCITY]

        flights.append({
            "callsign": callsign,
            "origin_country": state[ORIGIN_COUNTRY] or "N/A",
            "latitude": lat,
            "longitude": lon,
            "altitude": round(altitude, 1) if altitude is not None else None,
            "velocity": round(velocity, 1) if velocity is not None else None,
        })

    return flights


def filter_flights(flights, query):
    """
    Filter a list of flight dicts by callsign or origin_country.

    query: case-insensitive substring to search for.
           Returns the full list unchanged if query is empty or None.
    """
    if not query:
        return flights

    query_lower = query.lower()
    return [
        f for f in flights
        if query_lower in f["callsign"].lower()
        or query_lower in f["origin_country"].lower()
    ]
