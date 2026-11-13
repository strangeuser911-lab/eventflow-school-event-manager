from database.db import connect_database
from modules.helpers import get_integer, get_text
from modules.events import view_events
from modules.volunteers import view_volunteers

def assign_task():

    print("\n--- ASSIGN A TASK ---")

    view_events()
    event_id = get_integer("\nEnter event ID: ")

    view_volunteers()
    volunteer_id = get_integer("\nEnter volunteer ID: ")

    task_name = get_text("Enter task description: ")

    connection = connect_database()
    cursor = connection.cursor()

    # Check whether the event exists
    cursor.execute(
        "SELECT event_id FROM events WHERE event_id = ?",
        (event_id,)
    )

    event = cursor.fetchone()

    # Check whether the volunteer exists
    cursor.execute(
        "SELECT volunteer_id FROM volunteers WHERE volunteer_id = ?",
        (volunteer_id,)
    )

    volunteer = cursor.fetchone()

    if event is None:
        print("\nEvent ID does not exist.")

    elif volunteer is None:
        print("\nVolunteer ID does not exist.")

    else:
        cursor.execute("""
            INSERT INTO tasks
            (task_name, event_id, volunteer_id)
            VALUES (?, ?, ?)
        """, (task_name, event_id, volunteer_id))

        connection.commit()

        print("\nTask assigned successfully!")

    connection.close()


# ==========================================
# 9. VIEW ALL TASKS
# ==========================================

def view_tasks():

    print("\n--- ALL ASSIGNED TASKS ---")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            tasks.task_id,
            tasks.task_name,
            events.event_name,
            volunteers.volunteer_name,
            tasks.status

        FROM tasks

        JOIN events
        ON tasks.event_id = events.event_id

        JOIN volunteers
        ON tasks.volunteer_id = volunteers.volunteer_id

        ORDER BY tasks.task_id
    """)

    tasks = cursor.fetchall()

    connection.close()

    if not tasks:
        print("No tasks assigned.")
        return

    for task in tasks:
        print(
            f"\nTask ID: {task[0]}"
            f"\nTask: {task[1]}"
            f"\nEvent: {task[2]}"
            f"\nVolunteer: {task[3]}"
            f"\nStatus: {task[4]}"
        )





def complete_task():

    print("\n--- COMPLETE A TASK ---")

    view_tasks()

    task_id = get_integer("\nEnter task ID: ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE task_id = ?
    """, (task_id,))

    if cursor.rowcount == 0:
        print("\nTask ID not found.")

    else:
        connection.commit()
        print("\nTask marked as completed!")

    connection.close()
