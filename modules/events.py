from database.db import connect_database
from modules.helpers import get_integer, get_text, get_date, get_name

def add_event():

    print("\n--- ADD NEW EVENT ---")

    event_name = get_name("Enter event name: ")
    event_date = get_date("Enter event date (DD-MM-YYYY): ")
    venue = get_text("Enter venue: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM events
        WHERE event_name = ? AND event_date = ?
    """, (event_name, event_date))

    existing_event = cursor.fetchone()

    if existing_event:
        print("\nThis event already exists on that date.")
        connection.close()
        return

    cursor.execute("""
        INSERT INTO events (event_name, event_date, venue)
        VALUES (?, ?, ?)
    """, (event_name, event_date, venue))

    connection.commit()
    connection.close()

    print("\nEvent added successfully!")


# ==========================================
# 5. VIEW ALL EVENTS
# ==========================================

def view_events():

    print("\n--- ALL EVENTS ---")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM events")

    events = cursor.fetchall()

    connection.close()

    if not events:
        print("No events found.")
        return

    for event in events:
        print(
            f"\nID: {event[0]}"
            f"\nName: {event[1]}"
            f"\nDate: {event[2]}"
            f"\nVenue: {event[3]}"
        )

def search_events():
    print("\n--- SEARCH EVENTS ---")

    search_term = get_text("Enter event name to search: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM events
        WHERE event_name LIKE ?
    """, (f"%{search_term}%",))

    results = cursor.fetchall()
    connection.close()

    if not results:
        print("\nNo matching events found.")
        return

    print("\n--- SEARCH RESULTS ---")

    for event in results:
        print(
            f"\nID: {event[0]}"
            f"\nName: {event[1]}"
            f"\nDate: {event[2]}"
            f"\nVenue: {event[3]}"
        )


def edit_event():
    print("\n--- EDIT EVENT ---")

    view_events()

    event_id = get_integer("\nEnter the ID of the event to edit: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM events WHERE event_id = ?",
        (event_id,)
    )

    event = cursor.fetchone()

    if event is None:
        print("\nEvent ID not found.")
        connection.close()
        return

    print("\nEnter the updated details:")

    new_name = get_name("New event name: ")
    new_date = get_date("New event date (DD-MM-YYYY): ")
    new_venue = get_text("New venue: ")

    cursor.execute("""
        UPDATE events
        SET event_name = ?,
            event_date = ?,
            venue = ?
        WHERE event_id = ?
    """, (new_name, new_date, new_venue, event_id))

    connection.commit()
    connection.close()

    print("\nEvent updated successfully!")


def delete_event():
    print("\n--- DELETE EVENT ---")

    view_events()

    event_id = get_integer("\nEnter the ID of the event to delete: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM events WHERE event_id = ?",
        (event_id,)
    )

    event = cursor.fetchone()

    if event is None:
        print("\nEvent ID not found.")
        connection.close()
        return

    confirmation = input(
        f"Are you sure you want to delete '{event[1]}'? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":

        cursor.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE event_id = ?
            AND status != 'Completed'
        """, (event_id,))

        pending_tasks = cursor.fetchone()[0]

        if pending_tasks > 0:
            print("\nCannot delete this event!")
            print("Some tasks are still pending.")

        else:
            # Delete associated completed task records first
            cursor.execute(
                "DELETE FROM tasks WHERE event_id = ?",
                (event_id,)
            )

            # Now delete the event
            cursor.execute(
                "DELETE FROM events WHERE event_id = ?",
                (event_id,)
            )

            connection.commit()
            print("\nEvent deleted successfully!")

    else:
        print("\nDeletion cancelled.")




