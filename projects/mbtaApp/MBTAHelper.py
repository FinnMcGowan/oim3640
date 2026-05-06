from pathlib import Path
import os

from flask import Flask, render_template, request
import requests


BASE_DIR = Path(__file__).resolve().parent.parent


def load_env_file(env_path):
	"""Load key=value pairs from a .env file into environment variables."""
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue

		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip().strip('"').strip("'")

		if key and key not in os.environ:
			os.environ[key] = value


load_env_file(BASE_DIR / ".env")
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "").strip()
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN", "").strip()

app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent))


def geocode_place(place_query):
	"""Convert a place name into latitude/longitude using the Mapbox Geocoding API."""
	if not MAPBOX_TOKEN:
		raise ValueError("MAPBOX_TOKEN is missing. Add it to your .env file.")

	encoded = requests.utils.quote(place_query)
	url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{encoded}.json"
	params = {
		"access_token": MAPBOX_TOKEN,
		"limit": 1,
	}

	response = requests.get(url, params=params, timeout=10)
	response.raise_for_status()

	data = response.json()
	features = data.get("features") or []
	if not features:
		return None

	feature = features[0]
	lon, lat = feature["geometry"]["coordinates"]
	return {
		"latitude": lat,
		"longitude": lon,
		"display_name": feature.get("place_name", place_query),
	}


def get_nearest_station(latitude, longitude):
	"""Return nearest MBTA stop for latitude/longitude, or (None, error_message)."""
	if not MBTA_API_KEY:
		return None, "MBTA API key is missing. Add MBTA_API_KEY in your .env file."

	url = "https://api-v3.mbta.com/stops"
	params = {
		"filter[latitude]": latitude,
		"filter[longitude]": longitude,
		"sort": "distance",
		"page[limit]": 1,
	}
	headers = {"x-api-key": MBTA_API_KEY}

	try:
		response = requests.get(url, params=params, headers=headers, timeout=10)
		response.raise_for_status()
	except requests.RequestException:
		return None, "Could not reach MBTA API right now. Please try again."

	payload = response.json()
	data = payload.get("data") or []
	if not data:
		return None, "No nearby MBTA stations were found for those coordinates."

	stop = data[0]
	attributes = stop.get("attributes") or {}

	# wheelchair_boarding: 1 = accessible, 2 = not accessible, 0 = no info
	wb = attributes.get("wheelchair_boarding", 0)
	wheelchair_accessible = wb == 1

	return {
		"name": attributes.get("name", "Unknown Station"),
		"municipality": attributes.get("municipality", "Unknown Municipality"),
		"address": attributes.get("address", "Address not available"),
		"wheelchair_accessible": wheelchair_accessible,
		"wheelchair_boarding": wb,
		"latitude": attributes.get("latitude"),
		"longitude": attributes.get("longitude"),
	}, None


def find_stop_near(place_name):
	"""High-level helper: place name → (stop name, wheelchair_accessible)."""
	geo = geocode_place(place_name)
	if geo is None:
		return None, False
	station, error = get_nearest_station(geo["latitude"], geo["longitude"])
	if error or station is None:
		return None, False
	return station["name"], station["wheelchair_accessible"]


@app.get("/")
def home():
	return render_template(
		"StationFinder.html",
		result=None,
		error=None,
		place="",
		looked_up_place=None,
		geo=None,
		mapbox_token=MAPBOX_TOKEN,
	)


@app.post("/nearest-station")
def nearest_station():
	place = request.form.get("place", "").strip()
	if not place:
		return render_template(
			"StationFinder.html",
			result=None,
			error="Please enter your location (for example: Boston Common).",
			place="",
			looked_up_place=None,
			geo=None,
			mapbox_token=MAPBOX_TOKEN,
		)

	try:
		geo = geocode_place(place)
	except ValueError as e:
		return render_template(
			"StationFinder.html",
			result=None,
			error=str(e),
			place=place,
			looked_up_place=None,
			geo=None,
			mapbox_token=MAPBOX_TOKEN,
		)
	except requests.RequestException:
		return render_template(
			"StationFinder.html",
			result=None,
			error="Could not reach Mapbox. Please try again.",
			place=place,
			looked_up_place=None,
			geo=None,
			mapbox_token=MAPBOX_TOKEN,
		)

	if geo is None:
		return render_template(
			"StationFinder.html",
			result=None,
			error="Could not understand that location. Try a more specific place name.",
			place=place,
			looked_up_place=None,
			geo=None,
			mapbox_token=MAPBOX_TOKEN,
		)

	station, error = get_nearest_station(geo["latitude"], geo["longitude"])
	return render_template(
		"StationFinder.html",
		result=station,
		error=error,
		place=place,
		looked_up_place=geo["display_name"],
		geo=geo,
		mapbox_token=MAPBOX_TOKEN,
	)


if __name__ == "__main__":
	app.run(debug=True, use_reloader=False)
