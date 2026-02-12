# AppStore (Django)

A Django-based mini app store where users can browse and download approved APKs, and developers can upload and manage apps.

## Features

- User and developer registration
- Role-aware login flow
- Browse approved apps on home page
- Search apps by name
- App detail page
- Auth-required download tracking
- Developer-only app upload and delete
- User reviews on app detail page
- Media file handling for APK and app images

## Tech Stack

- Python 3
- Django 6.0.2
- SQLite (default)
- Pillow (image upload support)


## Setup

1. Create and activate a virtual environment (optional if already using one):

```terminal
python -m venv .venv
.\.venv\Scripts\activate
```

2. Install dependencies:

```terminal
pip install -r appstore/core/requirement.txt
```

3. Apply migrations:

```terminal
cd appstore
python manage.py migrate
```

4. (Optional) Create admin user:

```terminal
python manage.py createsuperuser
```

5. Run the development server:

```terminal
python manage.py runserver
```
