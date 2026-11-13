from database.db import connect_database, initialize_database
from modules.tasks import (
    assign_task,
    view_tasks,
    complete_task
)
from modules.volunteers import (
    register_volunteer,
    view_volunteers,
    edit_volunteer,
    delete_volunteer
)
from modules.events import (
    add_event,
    view_events,
    search_events,
    edit_event,
    delete_event
)
from modules.helpers import (
    get_integer,
    get_text,
    get_date,
    get_name
)
import sqlite3

# ==========================================
# EVENTFLOW - SCHOOL EVENT MANAGEMENT SYSTEM
# ==========================================

DATABASE_NAME = "eventflow.db"

# ==========================================
# MAIN MENU
# ==========================================

def main():

    initialize_database()

    print("\n================================")
    print("          EVENTFLOW")
    print("  SCHOOL EVENT MANAGEMENT")
    print("================================")

    while True:

        print("\nMAIN MENU")
        print("1. Add a new event")
        print("2. View all events")
        print("3. Register a volunteer")
        print("4. View all volunteers")
        print("5. Assign a task")
        print("6. View all tasks")
        print("7. Mark a task as completed")
        print("8. Exit")
        print("9. Search for an event")
        print("10. Edit an event")
        print("11. Delete an event")
        print("12. Edit volunteer details")
        print("13. Delete a volunteer")

        choice = input("\nEnter your choice (1-13): ").strip()

        if choice == "1":
            add_event()

        elif choice == "2":
            view_events()

        elif choice == "3":
            register_volunteer()

        elif choice == "4":
            view_volunteers()

        elif choice == "5":
            assign_task()

        elif choice == "6":
            view_tasks()

        elif choice == "7":
            complete_task()

        elif choice == "8":
            print("\nThank you for using EventFlow!")

        elif choice == "9":
            search_events()

        elif choice == "10":
            edit_event()

        elif choice == "11":
            delete_event()

        elif choice == "12":
            edit_volunteer()

        elif choice == "13":
            delete_volunteer()
            break

        else:
            print("\nInvalid choice. Please select 1-13.")

# ==========================================
#  PROGRAM ENTRY POINT
# ==========================================

if __name__ == "__main__":
    main()