import atexit


from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template, jsonify
from app.helper import get_data, get_categories, fetch_data
from config.config import config
from app.database import Database

app = Flask(__name__)
db = Database()

scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_data, trigger="cron", day_of_week="0-4", hour="9-16", minute="*/5", timezone='US/Eastern')
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_data")
def load_data():
    hard_update = True if request.args.get('refresh') == "1" else False
    data = get_data(hard_update)
    last_update = db.get_last_update()["last_update"]

    return [data, get_categories(), last_update]


@app.route("/add", methods =["GET", "POST"])
def add():
    categories = get_categories()

    if request.method == "POST":
        ticker = request.form.get("ticker")
        category = request.form.get("category")

        if category == 'Other':
            category = request.form.get("new-category")
        
        if category not in categories:
            db.add_category({
                "category": category,
                "stocks": [ticker]
            })
        else:
            stocks = db.fetchone("category", {"category": category})["stocks"]

            if ticker not in stocks:
                stocks.append(ticker)

            db.update("category", {"stocks": stocks}, {"category": category})

        return render_template("add_stocks.html", categories=categories, ticker=ticker, category=category)

    return render_template("add_stocks.html", categories=categories)
