"""
RUN |
The script to run the app without issues.
"""

from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    """
    Create tables.
    """
    db.create_all()
