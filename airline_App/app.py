from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from auth.models import User
from auth.routes import auth_bp
from extensions import db, login_manager
from utils.fetch_data import get_airline_data, analyze_data
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airline.db'

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    # If user is logged in, go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        # Show registration page by default
        return redirect(url_for('auth.register'))

@app.route('/dashboard')
@login_required
def index():
    data = get_airline_data()

    route_filter = request.args.get("route", "")
    start_date = request.args.get("start", "")
    end_date = request.args.get("end", "")

    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        data = [d for d in data if datetime.strptime(d["date"], "%Y-%m-%d") >= start_date]

    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        data = [d for d in data if datetime.strptime(d["date"], "%Y-%m-%d") <= end_date]

    if route_filter:
        data = [d for d in data if d["route"] == route_filter]

    available_routes = sorted(set(d["route"] for d in get_airline_data()))
    insights = analyze_data(data)
    flight_data_json = json.dumps(data)

    return render_template(
        'index.html',
        insights=insights,
        available_routes=available_routes,
        selected_route=route_filter,
        start_date=start_date.strftime('%Y-%m-%d') if start_date else "",
        end_date=end_date.strftime('%Y-%m-%d') if end_date else "",
        flight_data_json=flight_data_json
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create DB tables if they don't exist
    app.run(debug=True) 