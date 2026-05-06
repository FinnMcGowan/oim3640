from flask import Flask, jsonify, render_template, request

from api_helper import fetch_live_flights, filter_flights, parse_flight_data

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main map page."""
    return render_template("map.html")


@app.route("/api/flights")
def api_flights():
    """
    Return live flight data as JSON.

    Accepts an optional ?q= query parameter to filter results
    by callsign or origin country.
    """
    query = request.args.get("q", "").strip()

    raw_data = fetch_live_flights()
    flights = parse_flight_data(raw_data)
    flights = filter_flights(flights, query)

    return jsonify(flights)


if __name__ == "__main__":
    app.run(debug=True)
