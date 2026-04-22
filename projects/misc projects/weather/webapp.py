import os
from datetime import datetime, timedelta, timezone

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Weather Finder</title>
	<style>
		:root {
			--bg-a: #e6f7ff;
			--bg-b: #d4f0ff;
			--text: #0f2a3d;
			--accent: #0d6efd;
			--card: #ffffffcc;
			--danger: #b42318;
		}

		* { box-sizing: border-box; }

		body {
			margin: 0;
			min-height: 100vh;
			font-family: "Trebuchet MS", "Segoe UI", sans-serif;
			color: var(--text);
			background:
				radial-gradient(1100px 500px at 90% -10%, #a7e3ff 0%, transparent 60%),
				radial-gradient(900px 450px at -10% 110%, #b5f2e7 0%, transparent 60%),
				linear-gradient(160deg, var(--bg-a), var(--bg-b));
			display: grid;
			place-items: center;
			padding: 24px;
		}

		.card {
			width: min(680px, 95vw);
			background: var(--card);
			border: 1px solid #ffffff;
			backdrop-filter: blur(6px);
			border-radius: 16px;
			padding: 24px;
			box-shadow: 0 18px 40px rgba(13, 72, 115, 0.12);
			animation: rise 380ms ease-out;
		}

		h1 {
			margin-top: 0;
			margin-bottom: 10px;
			font-size: clamp(1.5rem, 3.8vw, 2rem);
			letter-spacing: 0.5px;
		}

		p.subtitle {
			margin-top: 0;
			color: #35576f;
		}

		form {
			display: flex;
			gap: 10px;
			flex-wrap: wrap;
			margin: 18px 0 8px;
		}

		input[type="text"] {
			flex: 1 1 320px;
			min-width: 220px;
			border: 1px solid #a9d3ea;
			border-radius: 10px;
			padding: 11px 12px;
			font-size: 1rem;
		}

		button {
			border: 0;
			border-radius: 10px;
			padding: 11px 15px;
			background: var(--accent);
			color: white;
			font-weight: 700;
			cursor: pointer;
			transition: transform 140ms ease, filter 140ms ease;
		}

		button:hover {
			transform: translateY(-1px);
			filter: brightness(1.05);
		}

		.result {
			margin-top: 16px;
			background: #ffffff;
			border-radius: 12px;
			padding: 14px 16px;
			border: 1px solid #d8ebf7;
		}

		.error {
			color: var(--danger);
			margin-top: 12px;
			font-weight: 600;
		}

		.small {
			color: #4b6d82;
			font-size: 0.95rem;
			margin: 4px 0;
		}

		@keyframes rise {
			from {
				opacity: 0;
				transform: translateY(8px);
			}
			to {
				opacity: 1;
				transform: translateY(0);
			}
		}
	</style>
</head>
<body>
	<main class="card">
		<h1>Weather Finder</h1>
		<p class="subtitle">Enter a city or location to get the latest weather.</p>

		<form method="post">
			<input
				type="text"
				name="location"
				value="{{ location|default('', true) }}"
				placeholder="Example: Boston, MA"
				required
			>
			<button type="submit">Get Weather</button>
		</form>

		{% if error %}
			<p class="error">{{ error }}</p>
		{% endif %}

		{% if weather %}
			<section class="result">
				<h2 style="margin: 0 0 6px 0;">{{ weather.display_name }}</h2>
				<p class="small">Temperature: <strong>{{ weather.temperature_c }}&deg;C</strong> ({{ weather.temperature_f }}&deg;F)</p>
				<p class="small">Wind Speed: <strong>{{ weather.wind_kph }} km/h</strong></p>
				<p class="small">Condition: <strong>{{ weather.description }}</strong></p>
				<p class="small">Time (local): {{ weather.time }}</p>
			</section>
		{% endif %}
	</main>
</body>
</html>
"""


def geocode_location(location):
		"""Return the first OpenWeather geocoding match (name, lat, lon)."""
		geocode_url = "http://api.openweathermap.org/geo/1.0/direct"
		response = requests.get(
				geocode_url,
				params={"q": location, "limit": 1, "appid": OPENWEATHER_API_KEY},
				timeout=10,
		)
		response.raise_for_status()
		results = response.json()

		if not results:
				return None

		match = results[0]
		city = match.get("name", "Unknown")
		state = match.get("state", "")
		country = match.get("country", "")

		pieces = [city]
		if state:
				pieces.append(state)
		if country:
				pieces.append(country)

		return {
				"display_name": ", ".join(pieces),
				"latitude": match.get("lat"),
				"longitude": match.get("lon"),
		}


def get_current_weather(latitude, longitude):
		"""Fetch current weather for the given coordinates from OpenWeatherMap."""
		forecast_url = "https://api.openweathermap.org/data/2.5/weather"
		response = requests.get(
				forecast_url,
				params={
						"lat": latitude,
						"lon": longitude,
						"appid": OPENWEATHER_API_KEY,
						"units": "metric",
				},
				timeout=10,
		)
		response.raise_for_status()
		payload = response.json()

		main_data = payload.get("main") or {}
		wind_data = payload.get("wind") or {}
		weather_list = payload.get("weather") or []
		temperature_c = main_data.get("temp")
		if temperature_c is None:
				return None

		wind_mps = wind_data.get("speed", 0)
		wind_kph = wind_mps * 3.6

		condition = "Unknown"
		if weather_list:
				condition = weather_list[0].get("description", "Unknown").title()

		observation_time = payload.get("dt")
		timezone_offset = payload.get("timezone", 0)
		local_time = "Unknown"
		if observation_time:
				local_time = datetime.fromtimestamp(
						observation_time,
						tz=timezone(timedelta(seconds=timezone_offset)),
				).strftime("%Y-%m-%d %H:%M")
		return {
				"temperature_c": round(temperature_c, 1),
				"temperature_f": round((temperature_c * 9 / 5) + 32, 1),
				"wind_kph": round(wind_kph, 1),
				"description": condition,
				"time": local_time,
		}


@app.route("/", methods=["GET", "POST"])
def index():
		location = ""
		weather = None
		error = None

		if request.method == "POST":
				location = request.form.get("location", "").strip()
				if not OPENWEATHER_API_KEY:
						error = "Set OPENWEATHER_API_KEY before running this app."
				elif not location:
						error = "Please enter a location."
				else:
						try:
								geo = geocode_location(location)
								if not geo:
										error = "Location not found. Try a different city or spelling."
								else:
										current = get_current_weather(geo["latitude"], geo["longitude"])
										if not current:
												error = "Weather data unavailable for that location right now."
										else:
												weather = {**geo, **current}
						except requests.HTTPError as exc:
								status = exc.response.status_code if exc.response is not None else None
								if status == 401:
										error = "OpenWeatherMap API key is invalid."
								else:
										error = "Could not reach OpenWeatherMap. Please try again shortly."
						except requests.RequestException:
								error = "Could not reach OpenWeatherMap. Please try again shortly."

		return render_template_string(
				HTML_TEMPLATE,
				location=location,
				weather=weather,
				error=error,
		)


if __name__ == "__main__":
		app.run(debug=True)
