import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-too")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/todo_events_test"
    TESTING = True
    DEBUG = True