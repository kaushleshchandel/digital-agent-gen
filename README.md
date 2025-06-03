# digital-agent-gen

This project contains a simple example of a Python API backend with a Flask based frontend.
The backend uses SQLite for storage and exposes a Swagger UI for testing.

## Structure

- `backend/` – FastAPI application exposing a REST API with user management.
- `frontend/` – Flask application serving HTML pages that call the API via JavaScript.

## Requirements

- Python 3.8+
- [Virtualenv](https://docs.python.org/3/library/venv.html)

## Setup

1. **Clone the repository** and open it in Visual Studio Code.
2. **Create a virtual environment** and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install backend dependencies**:

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Install frontend dependencies** (still inside the virtual environment):

   ```bash
   pip install -r frontend/requirements.txt
   ```

## Running the applications

Open two terminals in VS Code.

### Backend

Run the FastAPI backend (it listens on port `8000`):

```bash
uvicorn backend.main:app --reload
```

Swagger UI will be available at `http://localhost:8000/docs` for testing the API.

### Frontend

In the second terminal, start the Flask frontend (default port `5001`):

```bash
python frontend/app.py
```

The HTML pages served by Flask use client‑side JavaScript to communicate with the backend API.

## Features

- Register new users
- Login existing users (receives an API token)
- List users
- Delete users

All actions are performed through the API, providing a clear separation between frontend and backend.
