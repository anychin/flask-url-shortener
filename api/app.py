from flask import Flask
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)

application.config.update(
    DEBUG=True,
    SECRET_KEY='THIS_SHOULD_BE_SECRET',
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://babylon:babylon@database:5432/babylon',
)

db = SQLAlchemy(application)
