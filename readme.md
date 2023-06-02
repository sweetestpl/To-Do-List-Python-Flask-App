# Todo List Web Application

This is a simple web application built using Flask framework for managing a todo list. It allows users to create tasks, set due dates, update and delete tasks, and view tasks in a calendar format.

## Features

- User authentication: Users can register an account, log in, and log out.
- Create tasks: Users can add new tasks to their todo list.
- Set due dates: Users can specify start and end dates for their tasks.
- Update and delete tasks: Users can modify or remove existing tasks from their todo list.
- Calendar view: Users can view their tasks in a calendar format.

## Requirements

- Python 3.x
- Flask
- Flask_SQLAlchemy
- Flask_Login
- Werkzeug

## Installation and Setup

1. Clone this repository to your local machine.
2. Install the required dependencies using the following command:
   ```
   pip install -r requirements.txt
   ```
3. Run the application using the following command:
   ```
   python app.py
   ```
4. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. Register an account or log in if you already have an account.
2. Once logged in, you will see the todo list interface.
3. To add a new task, enter the task details in the input fields and click "Add Task".
4. To update or delete a task, click on the "Update" or "Delete" links next to the task.
5. To log out, click on the "Logout" link in the navigation bar.


## License

This project is licensed under the [MIT License](LICENSE).