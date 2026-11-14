import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_NAME = BASE_DIR / "eventflow.db"

def connect_database():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT NOT NULL,
            event_date TEXT NOT NULL,
            venue TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS volunteers (
            volunteer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_name TEXT NOT NULL,
            class_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            event_id INTEGER NOT NULL,
            volunteer_id INTEGER NOT NULL,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (event_id) REFERENCES events(event_id),
            FOREIGN KEY (volunteer_id) REFERENCES volunteers(volunteer_id)
        )
    """)

    connection.commit()
    connection.close()
