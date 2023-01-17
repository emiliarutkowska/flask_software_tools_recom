from datetime import datetime

import requests
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

import os
from models.models import Tool, Review, db


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

if not 'WEBSITE_HOSTNAME' in os.environ:
   print("Loading config.development and environment variables from .env file.")
   app.config.from_object('config.dev')
else:
   print("Loading config.production.")
   app.config.from_object('config.prod')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db.init_app(app)
migrate = Migrate(app, db)

GITHUB_URL = "https://api.github.com/user"
# from logging import getLogger
import logging

logging.basicConfig()
# LOGGER = getLogger(__name__)

def _get_current_user():
    user_token = request.headers.get("X-Ms-Token-Github-Access-Token")
    headers = {"Authorization": f"Bearer {user_token}"}
    response = requests.get(GITHUB_URL, headers=headers).json()

    user = {
        "login": response.get("login"),
        "name": response.get("name")
    }

    return user

@app.route('/', methods=['GET'])
def index():

    app.logger.debug("debug log info")
    app.logger.info("Info log information")
    app.logger.warning("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWarning log info")
    app.logger.error("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEError log info")
    app.logger.critical("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCritical log info")

    user = _get_current_user()
    print('Request for index page received')
    tools = Tool.query.all()
    return render_template('index.html',
                           tools=tools,
                           user_login=user.get("login"),
                           user_name=user.get("name"))


@app.route('/<int:id>', methods=['GET'])
def details(id):
    tool = Tool.query.where(Tool.id == id).first()
    reviews = Review.query.where(Review.tool_id == id)
    return render_template('details.html', tool=tool, reviews=reviews)


@app.route('/create', methods=['GET'])
def create_software_tool():
    print('Request for add tool received')
    return render_template('create_software_tool.html')


@app.route('/add', methods=['POST'])
@csrf.exempt
def add_software_tool():
    try:
        name = request.values.get('software_tool_name')
        link = request.values.get('website_link')
        description = request.values.get('description')
    except (KeyError):
        # Redisplay the question voting form.
        return render_template('add_software_tool.html', {
            'error_message': "You must include a tool name, link, and description",
        })
    else:
        tool = Tool(name, link, description)
        db.session.add(tool)
        db.session.commit()

        return redirect(url_for('details', id=tool.id))


@app.route('/review/<int:id>', methods=['POST'])
@csrf.exempt
def add_review(id):
    try:
        user_name = request.values.get('user_name')
        rating = request.values.get('rating')
        review_text = request.values.get('review_text')
    except (KeyError):
        # Redisplay the question voting form.
        return render_template('add_review.html', {
            'error_message': "Error adding review",
        })
    else:
        review = Review(tool_id=id, user_name=user_name, rating=rating, review_text=review_text)
        db.session.add(review)
        db.session.commit()

    return redirect(url_for('details', id=id))


@app.context_processor
def utility_processor():
    def star_rating(id):
        reviews = Review.query.where(Review.tool_id == id)

        ratings = []
        review_count = 0;
        for review in reviews:
            ratings += [review.rating]
            review_count += 1

        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        stars_percent = round((avg_rating / 5.0) * 100) if review_count > 0 else 0
        return {'avg_rating': avg_rating, 'review_count': review_count, 'stars_percent': stars_percent}

    return dict(star_rating=star_rating)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
   app.run()
