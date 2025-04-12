# Flask URL Shortener

A lightweight URL Shortener built with Flask and SQLite that supports **custom aliases** for your URLs.

## Features
- Custom short aliases for your URLs.
- Avoid duplicate entries for the same long URL.
- SQLite database for quick prototyping
- Deploy-ready with Render


## Tech Stack

- **Flask** - web framework
- **SQLite** - Lightweight database
- **SQLAlchemy** - ORM
- **Gunicorn** - Production WSGI server

## Getting started

### 1. Clone the repository
```bash
git clone https://github.com/Visvas07/url-shortener-flask.git
cd url-shortener-flask
```

### 2. Create virutal environment and install dependencies
```bash       
python -m venv venv
source venv/bin/activate # Windows:./venv/Scripts/activate
pip install -r requirements.txt
```

### 3. Run locally
```bash
python app.py
```
Visit http://localhost:5000

## Project Structure

```
.
├── app.py
├── models.py
├── templates/
│   └── index.html
├── instance/
│   └── yourdb.sqlite  # (generated after first run)
├── requirements.txt
├── Procfile
├── render.yaml
└── README.md
```

## License
MIT License

## Credits

Built using Flask and SQLite