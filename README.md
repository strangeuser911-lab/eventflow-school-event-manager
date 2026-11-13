
# EventFlow – School Event & Volunteer Management System

EventFlow is a web-based application developed to simplify the management of school events, volunteers, and assigned responsibilities.

The project is designed around the practical requirements of organising school events, where coordinators need to manage event details, register volunteers, distribute tasks, and monitor task completion.

## Features

### Event Management
- Add and view school events.
- Search events by name.
- Edit event details, including name, date, and venue.
- Delete events while preventing deletion if pending tasks exist.

### Volunteer Management
- Register and view volunteers.
- Search volunteers by name.
- Edit volunteer details.
- Delete volunteers while preventing deletion if pending tasks exist.

### Task Management
- Assign tasks to registered volunteers for specific events.
- View task assignments with associated event and volunteer details.
- Track task status as Pending or Completed.
- Mark pending tasks as completed.

### Dashboard
- View the total number of events.
- View the total number of registered volunteers.
- Monitor total and pending tasks.

### Data Validation
- Prevent empty form submissions.
- Check for duplicate event and volunteer records.
- Validate event dates.
- Use database relationships to maintain consistency between events, volunteers, and tasks.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic and backend |
| Flask | Web application framework |
| SQLite | Relational database |
| SQL | Database queries and operations |
| HTML | Webpage structure |
| CSS | User interface styling |
| Jinja2 | Dynamic HTML rendering |
| Git & GitHub | Version control and project hosting |

## Project Structure

```text
eventflow-school-event-manager/
│
├── app.py
├── main.py
│
├── database/
│   └── db.py
│
├── modules/
│   ├── events.py
│   ├── volunteers.py
│   ├── tasks.py
│   └── helpers.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── events.html
│   ├── event_form.html
│   ├── volunteers.html
│   ├── volunteer_form.html
│   ├── tasks.html
│   └── task_form.html
│
├── static/
│   └── style.css
│
└── eventflow.db
```

## Database Design

The application uses an SQLite relational database with three main tables:

- **Events:** Stores event names, dates, venues, and unique event IDs.
- **Volunteers:** Stores volunteer names, class details, and unique volunteer IDs.
- **Tasks:** Stores task descriptions, associated event IDs, volunteer IDs, and completion status.

Foreign keys connect tasks to their corresponding events and volunteers. SQL JOIN queries are used to retrieve task information alongside event and volunteer details.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/strangeuser911-lab/eventflow-school-event-manager.git
```

### 2. Navigate into the project directory

```bash
cd eventflow-school-event-manager
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Flask

```bash
pip install Flask
```

### 5. Run the application

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000

## Development Background

EventFlow was developed to explore how software can address practical organisational challenges in school events.

The project evolved from a command-line Python application into a Flask-based web application, introducing a web interface, relational database operations, and modular application structure.

## Repository

[View EventFlow on GitHub](https://github.com/strangeuser911-lab/eventflow-school-event-manager)
