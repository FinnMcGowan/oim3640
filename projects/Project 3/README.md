# Live Flight Tracker

A Flask web application that displays real-time aircraft positions on an interactive map using the [OpenSky Network API](https://opensky-network.org/) — completely free, no API key required.

## Features

- Live aircraft positions fetched from the OpenSky Network REST API
- Interactive [Leaflet.js](https://leafletjs.com/) map with clickable markers
- Popup details for each aircraft: callsign, country, altitude, and speed
- Search bar to filter aircraft by callsign or origin country
- Auto-refreshes flight data every 30 seconds

## Project Structure

```
Project 3/
    app.py              # Flask app with route definitions
    api_helper.py       # OpenSky API calls, parsing, and filtering
    templates/
        map.html        # Map UI with Leaflet.js and JavaScript logic
```

## How to Run

1. Install dependencies (Flask and requests):

```bash
pip install flask requests
```

2. Run the app from the `Project 3` directory:

```bash
python app.py
```

3. Open your browser and go to:

```
http://127.0.0.1:5000
```

## API

The app exposes one internal API endpoint used by the frontend:

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Renders the map page |
| `/api/flights` | GET | Returns live flight data as JSON |

The `/api/flights` endpoint accepts an optional `?q=` query parameter to filter results:

```
/api/flights?q=united states
/api/flights?q=UAL
```

## Data Fields

Each aircraft returned by the API includes:

| Field | Description |
|---|---|
| `callsign` | Flight callsign (e.g. `UAL123`) |
| `origin_country` | Country of registration |
| `latitude` | Current latitude |
| `longitude` | Current longitude |
| `altitude` | Geometric altitude in meters |
| `velocity` | Ground speed in m/s |

## Data Source

Flight data comes from the [OpenSky Network](https://opensky-network.org/), a community-based receiver network that provides free access to live ADS-B flight data. No account or API key is needed for anonymous access (rate limits apply).
