
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash
)
from database.db import connect_database
from datetime import datetime

app = Flask(__name__)
app.secret_key = "eventflow-development-key"


# ---------- HELPER FUNCTIONS ----------

def valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_form_value(field):
    return request.form.get(field, "").strip()


# ---------- DASHBOARD ----------

@app.route("/")
def home():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM events")
    event_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM volunteers")
    volunteer_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks")
    task_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE status = 'Pending'"
    )
    pending_count = cursor.fetchone()[0]

    connection.close()

    return render_template(
        "index.html",
        event_count=event_count,
        volunteer_count=volunteer_count,
        task_count=task_count,
        pending_count=pending_count
    )


# ---------- EVENTS ----------

@app.route("/events")
def events():
    search = request.args.get("search", "").strip()

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT event_id, event_name, event_date, venue
        FROM events
        WHERE event_name LIKE ?
        ORDER BY event_date
    """, ("%" + search + "%",))

    all_events = cursor.fetchall()
    connection.close()

    return render_template(
        "events.html",
        events=all_events,
        search=search
    )


@app.route("/add_event", methods=["GET", "POST"])
def add_event():
    if request.method == "POST":
        event_name = get_form_value("event_name")
        event_date = get_form_value("event_date")
        venue = get_form_value("venue")

        if not event_name or not event_date or not venue:
            flash("Please fill in every field.")
            return redirect(url_for("add_event"))

        if not valid_date(event_date):
            flash("Please enter a valid date.")
            return redirect(url_for("add_event"))

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT event_id FROM events
            WHERE event_name = ? AND event_date = ?
        """, (event_name, event_date))

        if cursor.fetchone():
            connection.close()
            flash("An event with this name and date already exists.")
            return redirect(url_for("add_event"))

        cursor.execute("""
            INSERT INTO events (event_name, event_date, venue)
            VALUES (?, ?, ?)
        """, (event_name, event_date, venue))

        connection.commit()
        connection.close()

        flash("Event added successfully!")
        return redirect(url_for("events"))

    return render_template(
        "event_form.html",
        heading="Add Event",
        event=None
    )


@app.route("/edit_event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT event_id, event_name, event_date, venue
        FROM events WHERE event_id = ?
    """, (event_id,))

    event = cursor.fetchone()

    if event is None:
        connection.close()
        flash("Event not found.")
        return redirect(url_for("events"))

    if request.method == "POST":
        event_name = get_form_value("event_name")
        event_date = get_form_value("event_date")
        venue = get_form_value("venue")

        if not event_name or not event_date or not venue:
            connection.close()
            flash("Please fill in every field.")
            return redirect(url_for("edit_event", event_id=event_id))

        if not valid_date(event_date):
            connection.close()
            flash("Please enter a valid date.")
            return redirect(url_for("edit_event", event_id=event_id))

        cursor.execute("""
            SELECT event_id FROM events
            WHERE event_name = ? AND event_date = ?
            AND event_id != ?
        """, (event_name, event_date, event_id))

        if cursor.fetchone():
            connection.close()
            flash("Another event already has this name and date.")
            return redirect(url_for("edit_event", event_id=event_id))

        cursor.execute("""
            UPDATE events
            SET event_name = ?, event_date = ?, venue = ?
            WHERE event_id = ?
        """, (event_name, event_date, venue, event_id))

        connection.commit()
        connection.close()

        flash("Event updated successfully!")
        return redirect(url_for("events"))

    connection.close()

    return render_template(
        "event_form.html",
        heading="Edit Event",
        event=event
    )


@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE event_id = ? AND status = 'Pending'
    """, (event_id,))

    pending_count = cursor.fetchone()[0]

    if pending_count > 0:
        connection.close()
        flash("Cannot delete this event because it has pending tasks.")
        return redirect(url_for("events"))

    cursor.execute(
        "SELECT event_id FROM events WHERE event_id = ?",
        (event_id,)
    )

    if cursor.fetchone() is None:
        connection.close()
        flash("Event not found.")
        return redirect(url_for("events"))

    cursor.execute("DELETE FROM tasks WHERE event_id = ?", (event_id,))
    cursor.execute("DELETE FROM events WHERE event_id = ?", (event_id,))

    connection.commit()
    connection.close()

    flash("Event deleted successfully!")
    return redirect(url_for("events"))


# ---------- VOLUNTEERS ----------

@app.route("/volunteers")
def volunteers():
    search = request.args.get("search", "").strip()

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT volunteer_id, volunteer_name, class_name
        FROM volunteers
        WHERE volunteer_name LIKE ?
        ORDER BY volunteer_name
    """, ("%" + search + "%",))

    all_volunteers = cursor.fetchall()
    connection.close()

    return render_template(
        "volunteers.html",
        volunteers=all_volunteers,
        search=search
    )


@app.route("/add_volunteer", methods=["GET", "POST"])
def add_volunteer():
    if request.method == "POST":
        volunteer_name = get_form_value("volunteer_name")
        class_name = get_form_value("class_name")

        if not volunteer_name or not class_name:
            flash("Please fill in every field.")
            return redirect(url_for("add_volunteer"))

        if not any(character.isalpha() for character in volunteer_name):
            flash("Please enter a valid volunteer name.")
            return redirect(url_for("add_volunteer"))

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT volunteer_id FROM volunteers
            WHERE volunteer_name = ? AND class_name = ?
        """, (volunteer_name, class_name))

        if cursor.fetchone():
            connection.close()
            flash("This volunteer is already registered in that class.")
            return redirect(url_for("add_volunteer"))

        cursor.execute("""
            INSERT INTO volunteers (volunteer_name, class_name)
            VALUES (?, ?)
        """, (volunteer_name, class_name))

        connection.commit()
        connection.close()

        flash("Volunteer registered successfully!")
        return redirect(url_for("volunteers"))

    return render_template(
        "volunteer_form.html",
        heading="Register Volunteer",
        volunteer=None
    )


@app.route("/edit_volunteer/<int:volunteer_id>", methods=["GET", "POST"])
def edit_volunteer(volunteer_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT volunteer_id, volunteer_name, class_name
        FROM volunteers WHERE volunteer_id = ?
    """, (volunteer_id,))

    volunteer = cursor.fetchone()

    if volunteer is None:
        connection.close()
        flash("Volunteer not found.")
        return redirect(url_for("volunteers"))

    if request.method == "POST":
        volunteer_name = get_form_value("volunteer_name")
        class_name = get_form_value("class_name")

        if not volunteer_name or not class_name:
            connection.close()
            flash("Please fill in every field.")
            return redirect(
                url_for("edit_volunteer", volunteer_id=volunteer_id)
            )

        if not any(character.isalpha() for character in volunteer_name):
            connection.close()
            flash("Please enter a valid volunteer name.")
            return redirect(
                url_for("edit_volunteer", volunteer_id=volunteer_id)
            )

        cursor.execute("""
            SELECT volunteer_id FROM volunteers
            WHERE volunteer_name = ? AND class_name = ?
            AND volunteer_id != ?
        """, (volunteer_name, class_name, volunteer_id))

        if cursor.fetchone():
            connection.close()
            flash("Another volunteer has the same name and class.")
            return redirect(
                url_for("edit_volunteer", volunteer_id=volunteer_id)
            )

        cursor.execute("""
            UPDATE volunteers
            SET volunteer_name = ?, class_name = ?
            WHERE volunteer_id = ?
        """, (volunteer_name, class_name, volunteer_id))

        connection.commit()
        connection.close()

        flash("Volunteer updated successfully!")
        return redirect(url_for("volunteers"))

    connection.close()

    return render_template(
        "volunteer_form.html",
        heading="Edit Volunteer",
        volunteer=volunteer
    )


@app.route("/delete_volunteer/<int:volunteer_id>", methods=["POST"])
def delete_volunteer(volunteer_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM tasks
        WHERE volunteer_id = ? AND status = 'Pending'
    """, (volunteer_id,))

    pending_count = cursor.fetchone()[0]

    if pending_count > 0:
        connection.close()
        flash("Cannot delete this volunteer because they have pending tasks.")
        return redirect(url_for("volunteers"))

    cursor.execute("""
        SELECT volunteer_id FROM volunteers WHERE volunteer_id = ?
    """, (volunteer_id,))

    if cursor.fetchone() is None:
        connection.close()
        flash("Volunteer not found.")
        return redirect(url_for("volunteers"))

    cursor.execute(
        "DELETE FROM tasks WHERE volunteer_id = ?",
        (volunteer_id,)
    )
    cursor.execute(
        "DELETE FROM volunteers WHERE volunteer_id = ?",
        (volunteer_id,)
    )

    connection.commit()
    connection.close()

    flash("Volunteer deleted successfully!")
    return redirect(url_for("volunteers"))


# ---------- TASKS ----------

@app.route("/tasks")
def tasks():
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
        JOIN events ON tasks.event_id = events.event_id
        JOIN volunteers ON tasks.volunteer_id = volunteers.volunteer_id
        ORDER BY tasks.task_id DESC
    """)

    all_tasks = cursor.fetchall()
    connection.close()

    return render_template("tasks.html", tasks=all_tasks)


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT event_id, event_name FROM events ORDER BY event_date
    """)
    all_events = cursor.fetchall()

    cursor.execute("""
        SELECT volunteer_id, volunteer_name, class_name
        FROM volunteers ORDER BY volunteer_name
    """)
    all_volunteers = cursor.fetchall()

    if request.method == "POST":
        task_name = get_form_value("task_name")
        event_id = get_form_value("event_id")
        volunteer_id = get_form_value("volunteer_id")

        if not task_name or not event_id or not volunteer_id:
            connection.close()
            flash("Please fill in every field.")
            return redirect(url_for("add_task"))

        cursor.execute(
            "SELECT event_id FROM events WHERE event_id = ?",
            (event_id,)
        )
        event_exists = cursor.fetchone()

        cursor.execute(
            "SELECT volunteer_id FROM volunteers WHERE volunteer_id = ?",
            (volunteer_id,)
        )
        volunteer_exists = cursor.fetchone()

        if not event_exists or not volunteer_exists:
            connection.close()
            flash("Please select a valid event and volunteer.")
            return redirect(url_for("add_task"))

        cursor.execute("""
            INSERT INTO tasks (task_name, event_id, volunteer_id, status)
            VALUES (?, ?, ?, 'Pending')
        """, (task_name, event_id, volunteer_id))

        connection.commit()
        connection.close()

        flash("Task assigned successfully!")
        return redirect(url_for("tasks"))

    connection.close()

    return render_template(
        "task_form.html",
        events=all_events,
        volunteers=all_volunteers
    )


@app.route("/complete_task/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tasks
        SET status = 'Completed'
        WHERE task_id = ? AND status = 'Pending'
    """, (task_id,))

    if cursor.rowcount == 0:
        flash("Task not found or already completed.")
    else:
        flash("Task marked as completed!")

    connection.commit()
    connection.close()

    return redirect(url_for("tasks"))


if __name__ == "__main__":
    app.run(debug=True)
