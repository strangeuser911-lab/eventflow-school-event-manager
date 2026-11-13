from database.db import connect_database
from modules.helpers import get_integer, get_text


def register_volunteer():

    print("\n--- REGISTER VOLUNTEER ---")

    volunteer_name = get_text("Enter volunteer name: ")
    class_name = get_text("Enter class (e.g. XI-A): ")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO volunteers (volunteer_name, class_name)
        VALUES (?, ?)
    """, (volunteer_name, class_name))

    connection.commit()
    connection.close()

    print("\nVolunteer registered successfully!")





def view_volunteers():

    print("\n--- ALL VOLUNTEERS ---")

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM volunteers")

    volunteers = cursor.fetchall()

    connection.close()

    if not volunteers:
        print("No volunteers registered.")
        return

    for volunteer in volunteers:
        print(
            f"\nID: {volunteer[0]}"
            f"\nName: {volunteer[1]}"
            f"\nClass: {volunteer[2]}"
        )




def edit_volunteer():
    print("\n--- EDIT VOLUNTEER ---")

    view_volunteers()

    volunteer_id = get_integer(
        "\nEnter the volunteer ID to edit: "
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM volunteers WHERE volunteer_id = ?",
        (volunteer_id,)
    )

    volunteer = cursor.fetchone()

    if volunteer is None:
        print("\nVolunteer ID not found.")
        connection.close()
        return

    print("\nEnter the updated details:")

    new_name = get_text("New volunteer name: ")
    new_class = get_text("New class: ")

    cursor.execute("""
        UPDATE volunteers
        SET volunteer_name = ?,
            class_name = ?
        WHERE volunteer_id = ?
    """, (new_name, new_class, volunteer_id))

    connection.commit()
    connection.close()

    print("\nVolunteer details updated successfully!")



def delete_volunteer():
    print("\n--- DELETE VOLUNTEER ---")

    view_volunteers()

    volunteer_id = get_integer(
        "\nEnter the volunteer ID to delete: "
    )

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM volunteers WHERE volunteer_id = ?",
        (volunteer_id,)
    )

    volunteer = cursor.fetchone()

    if volunteer is None:
        print("\nVolunteer ID not found.")
        connection.close()
        return

    confirmation = input(
        f"Delete volunteer '{volunteer[1]}'? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":

        cursor.execute("""
            SELECT COUNT(*)
            FROM tasks
            WHERE volunteer_id = ?
            AND status != 'Completed'
        """, (volunteer_id,))

        pending_tasks = cursor.fetchone()[0]

        if pending_tasks > 0:
            print("\nCannot delete this volunteer!")
            print("Some assigned tasks are still pending.")

        else:
            cursor.execute(
                "DELETE FROM tasks WHERE volunteer_id = ?",
                (volunteer_id,)
            )

            cursor.execute(
                "DELETE FROM volunteers WHERE volunteer_id = ?",
                (volunteer_id,)
            )

            connection.commit()
            print("\nVolunteer deleted successfully!")

    else:
        print("\nDeletion cancelled.")

    connection.close()
