from datetime import datetime
def get_integer(prompt):

    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print("Please enter a valid number.")


def get_text(prompt):

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_name(prompt):
    while True:
        name = input(prompt).strip()

        if not name:
            print("Name cannot be empty.")

        elif not any(char.isalpha() for char in name):
            print("Please enter a valid name.")

        else:
            return name

def get_name(prompt):
    while True:
        name = input(prompt).strip()

        if not name:
            print("Name cannot be empty.")

        elif not any(char.isalpha() for char in name):
            print("Please enter a valid name.")

        else:
            return name

from datetime import datetime

def get_date(prompt):
    while True:
        date = input(prompt).strip()

        try:
            datetime.strptime(date, "%d-%m-%Y")
            return date

        except ValueError:
            print("Invalid date! Please use DD-MM-YYYY.")

