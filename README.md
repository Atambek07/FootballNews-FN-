
# Football News Feed

## Description

Football News Feed is a Django web application that collects and serves fresh football news from popular RSS feeds and open APIs.  
The application provides a REST API for accessing news with filtering options by football teams and leagues.

---

## Features

- Automatic parsing of news from at least 3 RSS sources.
- Storage of news, teams, and leagues in the database.
- REST API to retrieve news with filtering by teams and leagues.
- Django admin panel for content management.
- Management command for manual news update.
- Error handling when sources are unavailable.

---

## Technologies

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- feedparser (for RSS parsing)  
- PostgreSQL / SQLite (optional)

---

## Installation and Running

1. Clone the repository:

   ```bash
   git clone https://github.com/Atambek07/FootballNews-FN-.git
   cd football-news-feed
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate   # Windows

   pip install -r requirements.txt
   ```

3. Configure the database in `settings.py` (SQLite by default).

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser for admin access:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

7. Open in your browser:  
   - Admin panel: http://localhost:8000/admin/  
   - News API: http://localhost:8000/api/news/

---

## Usage

- To get news list with filters, send GET request to `/api/news/` with query parameters:

  - `teams` — comma-separated list of teams, e.g. `teams=Barcelona,Real`
  - `leagues` — comma-separated list of leagues, e.g. `leagues=La_Liga,Premier_League`

  Example:  
  `http://localhost:8000/api/news/?teams=Barcelona&leagues=La_Liga`

- Manual news update command:

  ```bash
  python manage.py fetch_news
  ```
---

## Planned Improvements

- Automate news updates with Celery or cron jobs.
- Add full-text search for news.
- Build a frontend using React or Vue.js.
- Expand news sources.

---

## Contact

For questions or suggestions, contact [atambek165@gmail.com].

---

