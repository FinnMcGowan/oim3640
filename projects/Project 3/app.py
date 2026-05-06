from flask import Flask, jsonify, render_template, request

from api_helper import fetch_live_flights, filter_flights, parse_flight_data

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main map page."""
    return render_template("map.html")


@app.route("/api/aircraft/<icao24>")
def api_aircraft(icao24):
    """
    Proxy endpoint that fetches aircraft metadata (type, registration)
    from hexdb.io using the ICAO24 transponder address.
    """
    import re
    import requests as req
    if not re.fullmatch(r'[0-9a-fA-F]{6}', icao24):
        return jsonify({"error": "invalid icao24"}), 400
    try:
        resp = req.get(f"https://hexdb.io/api/v1/aircraft/{icao24}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return jsonify({
                "type": data.get("Type", "N/A"),
                "registration": data.get("Registration", "N/A"),
                "operator": data.get("RegisteredOwners", "N/A"),
            })
    except Exception:
        pass
    return jsonify({"type": "N/A", "registration": "N/A", "operator": "N/A"})


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
