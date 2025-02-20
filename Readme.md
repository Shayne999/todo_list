# To Do List 

This is a simple to do list built with Django. It allows users to create, update, retrive and delete tasks created. It has user authentication, role based access control, logging, and structured error handling.

## Features
* User registration (staff and admin) and JWT authentication
* Task management operations: Create, Retrive, Update, and Delete
* Progress Tracking: Predefined task states (Pending, In Progress, Completed)
* Error logging and structured error handling
* PostgreSQL remote database
  
## Installation
### Prerequisites
* python 3.11+
* PostgreSQL

1. Clone The repositody
2. Install dependencies using the requirements.txt file
3. Set up a PostgreSQL database
4. Access Endpoints
    ### Authentication

    | Endpoint     | Method | Description                      |
    | ------------ | ------ | -------------------------------- |
    | `/register/` | POST   | Register a new user              |
    | `/login/`    | POST   | Obtain access and refresh tokens |
    | `/logout/`   | POST   | Log out a user                   |

    ### Task Management

    | Endpoint              | Method | Description                                     |
    | --------------------- | ------ | ----------------------------------------------- |
    | `/tasks/`             | GET    | List all tasks (Admin) / User's tasks (Regular) |
    | `/tasks/{id}/`        | GET    | Retrieve a specific task                        |
    | `/tasks/create/`      | POST   | Create a new task                               |
    | `/tasks/{id}/update/` | PUT    | Update a task (including status)                |
    | `/tasks/{id}/delete/` | DELETE | Delete a task                                   |

### User registration and login

```json
{
  "username": "testuser",
  "password": "securepassword"
}
```

### Task creation and update

```json
{
  "title": "task name",
  "description": "Task description",
  "due_date": "date",
  "status": "project progress status"
}
```

## Author
Shayne Ndlovu



