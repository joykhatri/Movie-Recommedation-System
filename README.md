# Movie Recommedation System

## 🚀 Setup Instructions

### 1️⃣ Create Virtual Environment
```bash
python -m venv .venv
```

### 2️⃣ Activate Virtual Environment
```bash
.venv\Scripts\activate
```

### Linux/macOS:
```bash
source .venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install django djangorestframework
pip install mysqlclient
pip install pandas
pip install requests apscheduler
```

### 4️⃣ Start Django Project & App
```bash
django-admin startproject movie_project .
django-admin startapp movie_app
```

### 5️⃣ Add Apps to INSTALLED_APPS (project/settings.py)
```bash
INSTALLED_APPS = [
    ...
    'rest_framework',
    'movie_app',
]
```

### 6️⃣ Configure MySQL Database (settings.py)
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',   # Or your DB host
        'PORT': '3306',
    }
}
```

### 7️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8️⃣ Run Server
### Development server:
```bash
python manage.py runserver
```

## 🔑 API Endpoints

### Fetch Content
| Method | Endpoint                                            | Description                              |
| ------ | --------------------------------------------------- | ---------------------------------------- |
| GET    | `/api/trending/`                                    | Get Trending Content                     |
| GET    | `/api/trending/?media_type=movie`                   | Get Trending Movies                      |
| GET    | `/api/trending/?media_type=tv`                      | Get Trending TV Series                   |
| GET    | `/api/actor/`                                       | Get Popular Actor                        |
| GET    | `/api/popular_content/`                             | Get Popular Content                      |
| GET    | `/api/popular_content/?media_type=movie`            | Get Popular Movies                       |
| GET    | `/api/popular_content/?media_type=tv`               | Get Popular TV Series                    |
| GET    | `/api/upcoming_content/`                            | Get Upcoming Content                     |
| GET    | `/api/upcoming_content/?media_type=movie`           | Get Upcoming Movies                      |
| GET    | `/api/upcoming_content/?media_type=tv`              | Get Upcoming TV Series                   |
| GET    | `/api/popular_content/?genres=Action`               | Filter Popular Content by Genres         |
| GET    | `/api/top_rated_content/`                           | Get Top Rated Content                    |
| GET    | `/api/tv_show_season/`                              | TV Show Season Deatils                   |
| GET    | `/api/season_episodes/?tv_id=45926&season_number=8` | TV Show Seasons Episodes Details         |
