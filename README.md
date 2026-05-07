# MovieWebApp

A minimal Flask-based movie collection web application using Server-Side Rendering (SSR).

## Features

- Users can create movie collections
- Collections are stored in a database
- Auth-less design:
  - Any visitor can create users
  - Any visitor can modify existing collections
- Movies can be:
  - Added
  - Renamed
  - Removed
- No ownership or permission checks
- Movie data is fetched from the OMDb API based on the movie title

---

## Setup

### 1. Create a Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install all required packages from requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Create the .env File

Create a .env file based on the provided .env.example:

```bash
cp .env.example .env
```
Or manually copy the contents.

### 4. Configure the Database File

Make sure the database file path matches the value configured inside .env.

Example:
```env
DATABASE_URL=sqlite:///movies.db
```
In this case, the SQLite database file should be:
movies.db
located in the project root directory.

## Running the Application

```bash
flask run
```
or
```bash
python3 app.py
```

## OMDb API
This project uses the OMDb API to fetch movie information when adding a movie by title.

You need an API key from: https://www.omdbapi.com/.

Add it to your .env file:

```env
OMDB_API_KEY=your_api_key
```

## Tech Stack

- Python
- Flask
- SQLite
- Jinja2
- OMDb API

## Notes

This project intentionally does **not** implement authentication or authorization checks.

All users and movie collections are publicly editable.