# Yacut

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-black)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Pytest](https://img.shields.io/badge/Pytest-tested-green)

Yacut is a URL shortening service with a web interface and REST API.

The service converts long URLs into short links, supports custom aliases and redirects users from short links to original URLs.

---

## Main features

- Generate short links automatically
- Create custom short aliases
- Redirect short links to original URLs
- REST API for integrations
- Web interface with forms
- Request validation
- API error handling with JSON responses
- SQLAlchemy database model
- Flask-Migrate support
- Automated tests with Pytest

---

## Tech stack

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- Flask-WTF
- Flask-Migrate
- Jinja2
- Pytest
- Flake8

---

## Project structure

```text
yacut/
├── yacut/
│   ├── __init__.py          # Application and database initialization
│   ├── api_views.py         # REST API endpoints
│   ├── constants.py         # Project constants
│   ├── error_handlers.py    # Error handling
│   ├── forms.py             # WTForms forms
│   ├── models.py            # SQLAlchemy models
│   ├── templates/           # HTML templates
│   ├── utils.py             # Short link generation utilities
│   └── views.py             # Web views
├── tests/                   # Automated tests
├── openapi.yml              # API schema
├── settings.py              # Application config
└── requirements.txt
```

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/id/` | Create a short link |
| `GET` | `/api/id/{short_id}/` | Get original URL by short ID |

---

## API examples

### Create short link

Request:

```http
POST /api/id/
Content-Type: application/json
```

```json
{
  "url": "https://example.com/some/very/long/url",
  "custom_id": "example"
}
```

Response:

```json
{
  "url": "https://example.com/some/very/long/url",
  "short_link": "http://localhost/example"
}
```

### Get original URL

```http
GET /api/id/example/
```

Response:

```json
{
  "url": "https://example.com/some/very/long/url"
}
```

---

## Local installation

Clone the repository:

```bash
git clone https://github.com/Viocid/yacut.git
cd yacut
```

Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux / macOS
venv\Scripts\activate         # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```env
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=your-secret-key
```

Apply migrations:

```bash
flask db upgrade
```

Run the application:

```bash
flask run
```

The service will be available at:

```text
http://127.0.0.1:5000
```

---

## Running tests

```bash
pytest
```

---

## What this project demonstrates

- Flask application structure
- REST API development
- SQLAlchemy model design
- Input validation
- Error handling
- Web forms with Flask-WTF
- Short ID generation logic
- Automated testing
