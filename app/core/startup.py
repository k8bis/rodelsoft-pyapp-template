from app.core.db import wait_for_db

def startup():
    wait_for_db()