install directly with pip:

pip install Flask Flask-Login Flask-SQLAlchemy Werkzeug pandas 


for accessing opensky data with rest api

pip install requests
pip install opensky-api


Create virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate       # On Linux/Mac
venv\Scripts\activate    

Install dependencies


pip install -r requirements.txt


Initialize the database

python
>>> from app import db
>>> db.create_all()
>>> exit()


python app.py
Visit your app at: http://127.0.0.1:5000