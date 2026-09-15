# 📝 NotesApp — Full-Stack Notes Management System

A clean, beginner-friendly full-stack notes app built with **Flask**
(Python) on the backend, **PostgreSQL** for storage, and plain
**HTML, CSS, and JavaScript** on the frontend — no frontend frameworks.

Every user gets their own private, password-protected space to create,
organize, search, pin, and favorite notes.

---

## ✨ Features

- User registration & login with secure, salted password hashing
- Session-based authentication (via Flask-Login)
- Create, view, edit, and delete notes
- Search notes by title or content
- Organize notes into custom categories
- Pin important notes to the top of the list
- Mark notes as favorites and filter by favorites
- Automatic created/updated timestamps
- Responsive dashboard that works on desktop and mobile
- Every user can only ever see or modify **their own** notes

---

## 🧱 Tech Stack

| Layer          | Technology                                   |
|-----------------|----------------------------------------------|
| Backend         | Python 3, Flask                              |
| Database        | PostgreSQL, via Flask-SQLAlchemy (ORM)       |
| Authentication  | Flask-Login (server-side sessions)           |
| Password hashing| Werkzeug's `generate_password_hash` (PBKDF2) |
| Frontend        | HTML5, CSS3, vanilla JavaScript (`fetch()`)  |

---

## 📁 Project Structure

```
notes-management-system/
├── app.py                  # Application factory — creates and wires up the Flask app
├── config.py                # All configuration, loaded from environment variables
├── seed_data.py              # One-time script: creates tables + demo data
├── requirements.txt          # Python dependencies
├── .env.example              # Template for your local environment variables
├── .gitignore
│
├── database/
│   └── db.py                 # The single shared SQLAlchemy `db` instance
│
├── models/                   # SQLAlchemy ORM models (one table each)
│   ├── user.py                # User account + password hashing methods
│   ├── category.py            # A note category, scoped to one user
│   └── note.py                # The core Note model
│
├── services/                 # Business logic, kept separate from HTTP routing
│   ├── auth_service.py        # Registration/login validation & rules
│   └── note_service.py        # Note CRUD, search/filter, ownership checks
│
├── routes/                   # Flask blueprints (the actual URL endpoints)
│   ├── page_routes.py          # Serves the HTML pages (dashboard, login, etc.)
│   ├── auth_routes.py          # /api/auth/*  — register, login, logout, me
│   ├── note_routes.py          # /api/notes/* — CRUD + pin/favorite
│   └── category_routes.py      # /api/categories/*
│
├── templates/                 # Jinja2 HTML templates (page shells)
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── create_note.html
│   ├── edit_note.html
│   ├── view_note.html
│   └── partials/
│       └── header.html         # Shared nav bar, included on every logged-in page
│
└── static/
    ├── css/
    │   └── style.css            # All styling — one file, no framework
    └── js/
        ├── app.js                # Shared helpers: apiRequest(), formatting, logout
        ├── auth.js                # Login & register form handling
        ├── dashboard.js           # Note grid, search, filters, categories
        ├── note_form.js           # Shared logic for Create Note & Edit Note pages
        └── view_note.js           # Single-note read-only view logic
```

### How the pieces fit together

The app is deliberately split into four layers, each with one job:

1. **Models** (`models/`) define the database tables and know nothing
   about HTTP — just data and simple helper methods (e.g. hashing a
   password, converting a row to a dictionary).
2. **Services** (`services/`) contain the actual business rules
   ("a title is required", "a user can only edit their own note") and
   talk to the database through the models. They raise plain Python
   exceptions (`AuthError`, `NoteError`) on failure.
3. **Routes** (`routes/`) are thin — they read the incoming request,
   call a service function, and turn the result (or the exception)
   into a JSON response with the right HTTP status code. This is the
   *only* layer that knows about Flask requests/responses.
4. **Templates + static/** are the frontend: server-rendered HTML
   shells that immediately call the JSON API with `fetch()` to load
   real data and handle user interaction — no page reloads after the
   initial load.

This layering means you can test or reason about "can this user
delete this note?" in `note_service.py` without touching Flask at
all, and you can change how a page looks without touching any Python.

---

## 🔒 How authentication & security work

- Passwords are **never stored in plain text**. `User.set_password()`
  runs the password through Werkzeug's `generate_password_hash`
  (PBKDF2-SHA256 with a random salt) before saving it, and
  `User.check_password()` verifies a login attempt against that hash.
- Login sessions are handled by **Flask-Login**, which stores a signed,
  tamper-proof user ID in an HTTP-only cookie. JavaScript can't read
  it, and it can't be modified without invalidating the signature.
- Every note/category API route is wrapped in `@login_required` and,
  under the hood, every database query in `note_service.py` filters
  `WHERE user_id = <the logged-in user's id>`. This means even if a
  user guesses another user's note ID in the URL, the query simply
  won't find a match and the API returns `404 Not Found` — one user
  can never read or modify another user's data.

---

## 🚀 Setup & Installation

### 1. Prerequisites

- Python 3.9+
- PostgreSQL installed and running locally (or a remote instance)

### 2. Get the project files

Copy the project folder to your machine (or `git clone` it if you've
pushed it to a repository), then open a terminal inside it:

```bash
cd notes-management-system
```

### 3. Create a virtual environment and install dependencies

```bash
python -m venv venv

# Activate it:
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

### 4. Create the PostgreSQL database

```bash
# Using the psql command line:
psql -U postgres -c "CREATE DATABASE notes_db;"
```

(Or create a database named `notes_db` — or any name you like — using
your preferred PostgreSQL GUI tool, e.g. pgAdmin.)

### 5. Configure environment variables

Copy the example file and edit it with your own values:

```bash
cp .env.example .env
```

Open `.env` and set:

```
SECRET_KEY=some-long-random-string
DATABASE_URL=postgresql://<your_pg_username>:<your_pg_password>@localhost:5432/notes_db
```

### 6. Initialize the database (create tables + demo data)

```bash
python seed_data.py
```

This creates all the tables and, the first time you run it, adds a
demo account so you can log in immediately:

```
email:    demo@example.com
password: demo1234
```

### 7. Run the application

```bash
python app.py
```

Open your browser to **http://localhost:5000** — you'll land on the
login page. Log in with the demo account above, or register a new one.

---

## 📡 API Reference

All endpoints below are prefixed with `/api` and return JSON. Endpoints
marked 🔒 require an active login session.

| Method | Endpoint                    | Description                              |
|--------|------------------------------|-------------------------------------------|
| POST   | `/api/auth/register`         | Create a new account                      |
| POST   | `/api/auth/login`             | Log in, starts a session                  |
| POST   | `/api/auth/logout` 🔒         | End the current session                   |
| GET    | `/api/auth/me` 🔒             | Get the current logged-in user            |
| GET    | `/api/notes` 🔒               | List the current user's notes (supports `?search=`, `?category_id=`, `?favorite=true`) |
| POST   | `/api/notes` 🔒               | Create a new note                         |
| GET    | `/api/notes/<id>` 🔒          | Get one note by ID                        |
| PUT    | `/api/notes/<id>` 🔒          | Update a note                             |
| DELETE | `/api/notes/<id>` 🔒          | Delete a note                             |
| PATCH  | `/api/notes/<id>/pin` 🔒      | Toggle a note's pinned status             |
| PATCH  | `/api/notes/<id>/favorite` 🔒 | Toggle a note's favorite status           |
| GET    | `/api/categories` 🔒          | List the current user's categories        |
| POST   | `/api/categories` 🔒          | Create a new category                     |

Every error response has the shape `{"error": "human-readable message"}`
with an appropriate HTTP status code (`400` for bad input, `401` for
not logged in, `404` for missing/not-yours, `500` for server errors).

---

## 🖥️ Page Routes

| URL                     | Page                                     |
|--------------------------|-------------------------------------------|
| `/`                      | Redirects to `/dashboard` or `/login`     |
| `/login`                  | Log in                                    |
| `/register`                | Create an account                         |
| `/dashboard` 🔒            | Your notes, with search & filters         |
| `/notes/create` 🔒          | Create a new note                         |
| `/notes/<id>` 🔒            | View a single note                        |
| `/notes/<id>/edit` 🔒        | Edit a note                               |

---

## 🛠️ Troubleshooting

- **`could not connect to server` / connection refused** — make sure
  PostgreSQL is actually running, and that the host/port/username/
  password in `DATABASE_URL` inside `.env` are correct.
- **`database "notes_db" does not exist`** — you skipped step 4; run
  the `CREATE DATABASE` command above (or create it via your GUI tool).
- **`relation "users" does not exist`** — the tables haven't been
  created yet; run `python seed_data.py`.
- **Port 5000 already in use** — another process (on macOS, often
  AirPlay Receiver) is using port 5000. Either stop it, or run with a
  different port: `app.run(debug=True, port=5001)` in `app.py`.
- **Changes to `.env` don't seem to apply** — restart `python app.py`;
  environment variables are only read once, at startup.

---

## 🔮 Ideas for extending this project

- Add pagination to the notes list for users with hundreds of notes
- Add a "share note" feature between users
- Rich text / Markdown support in the note editor
- Password reset via email
- Export notes to PDF or plain text
