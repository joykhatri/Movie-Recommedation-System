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
