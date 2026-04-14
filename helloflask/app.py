from pathlib import Path

from flask import Flask, render_template, request
import yfinance as yf

BASE_DIR = Path(__file__).resolve().parent.parent
app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))

@app.get("/")
def hello():
    return render_template("stock-form.html", price=None, symbol="", error=None)

@app.get("/ticker")
def ticker_get():
    return render_template("stock-form.html", price=None, symbol="", error=None)

@app.post("/ticker")
def ticker_post():
    symbol = request.form.get("symbol", "").strip().upper()
    if not symbol:
        return render_template(
            "stock-form.html",
            price=None,
            symbol="",
            error="Please enter a stock symbol.",
        )

    price = get_price(symbol)
    if price is None:
        return render_template(
            "stock-form.html",
            price=None,
            symbol=symbol,
            error="Could not find price data for that symbol.",
        )

    return render_template("stock-form.html", price=price, symbol=symbol, error=None)


def get_price(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d")
    if data.empty:
        return None
    return float(data["Close"].iloc[-1])


if __name__ == '__main__':
    app.run(debug=True)