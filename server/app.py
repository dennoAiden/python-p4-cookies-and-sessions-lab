#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from flask_cors import CORS


from models import db, Article, User

app = Flask(__name__)
CORS(app)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles',methods=['GET'])
def index_articles():
    # Query all articles from the database
    articles = Article.query.all()

    # Check if articles exist
    if not articles:
        return make_response(jsonify({"message": "No articles found"}), 404)

    # Convert each article to a dictionary and return as JSON
    articles_json = [article.to_dict() for article in articles]

    return make_response(jsonify(articles_json), 200)

@app.route('/articles/<int:id>',methods=['GET'])
def show_article(id):
    # Fetch the article by id using the SQLAlchemy 2.0+ approach
    article = db.session.get(Article, id)

    if not article:
        return make_response(jsonify({"message": "Article not found"}), 404)

    # Initialize page_views to 0 if not already set
    session['page_views'] = session.get('page_views', 0)

    # Increment page_views
    session['page_views'] += 1

    # Check if the user has viewed more than 3 pages
    if session['page_views'] > 3:
        return make_response(
            jsonify({"message": "Maximum pageview limit reached"}), 401
        )

    # If within page views limit, return the article data
    return make_response(jsonify(article.to_dict()), 200)
