# Instructions
- Build a web application using Flask that connects to external APIs. Create something interactive that displays real data on a map or in a useful interface.


# Proposal:

## What I'm building:
A Flask web application that displays live flight data on an interactive map. The app will use the OpenSky Network API (free, no key required) to fetch real-time aircraft positions and show them as markers on a map with details like flight number, altitude, speed, and origin country.

## Why I chose this:
I use flightrader24, and I think it would be fun to see where flight data comes from, and use what I have learned from the course to build a similar tool. 

## Core features:
- Connect to the OpenSky Network REST API to fetch live aircraft state vectors
- Parse the JSON response and extract key fields: callsign, latitude, longitude, altitude, velocity, and origin country
- Display aircraft positions as interactive markers on a Leaflet.js map embedded in the Flask template
- Show a popup on each marker with flight details when clicked
- Add a filter input so the user can search by country or callsign
- Auto-refresh the map data every 30 seconds using a meta refresh or JavaScript fetch

## What I don't know yet:
- How to pass a large number of map markers from Flask to the Jinja2 template efficiently
- Whether to render the map server-side or use JavaScript fetch to pull data from a Flask API endpoint
- How to handle aircraft with missing or null position data from the API
- How to keep the map centered and zoomed while still updating marker positions
