# 📝 Blog Platform — REST API

A full-featured Blog Platform REST API built with Django REST Framework.

---

## 🛠 Tech Stack

| Technology                    | Version   | Purpose                          |
|-------------------------------|-----------|----------------------------------|
| Python                        | 3.12+     | Programming language             |
| Django                        | 5.2+      | Web framework                    |
| Django REST Framework         | 3.17+     | REST API toolkit                 |
| SimpleJWT                     | 5.5+      | Bearer token authentication      |
| SQLite                        | —         | Default database                 |
| django-filter                 | 25.1+     | Filtering support                |
| django-cors-headers           | 4.7+      | CORS handling                    |
| drf-spectacular               | 0.28+     | OpenAPI 3 / Swagger UI / ReDoc   |
| Pillow                        | 12.0+     | Image uploads                    |
| python-decouple               | 3.8+      | .env configuration               |

---

## 📁 Project Structure

```
exam-7-n73/
│
├── core/                            # Django project config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── apps/
│   ├── __init__.py
│   ├── permissions.py               # Custom permissions (IsAuthorOrReadOnly)
│   ├── urls/
│   │   ├── __init__.py
│   │   └── v1.py                    # Central v1 API router
│   │
│   ├── users/                       # Auth & user management
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   ├── urls/
│   │   │   ├── __init__.py
│   │   │   └── v1.py
│   │   └── migrations/
│   │       └── __init__.py
│   │
│   ├── posts/                       # Blog posts & categories
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── tests.py
│   │   ├── urls/
│   │   │   ├── __init__.py
│   │   │   └── v1.py
│   │   └── migrations/
│   │       └── __init__.py
│   │
│   └── comments/                    # Comments & reactions
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── serializers.py
│       ├── admin.py
│       ├── apps.py
│       ├── tests.py
│       ├── urls/
│       │   ├── __init__.py
│       │   └── v1.py
│       └── migrations/
│           └── __init__.py
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd exam-7-n73
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root (or edit the provided one):

```dotenv
SECRET_KEY=django-insecure-change-me-in-production-abc123xyz
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## ⚙️ Environment Variables

| Variable               | Type   | Default                                          | Description                     |
|------------------------|--------|--------------------------------------------------|---------------------------------|
| `SECRET_KEY`           | String | `django-insecure-change-me`                      | Django secret key               |
| `DEBUG`                | Bool   | `True`                                           | Debug mode                      |
| `ALLOWED_HOSTS`        | CSV    | `localhost,127.0.0.1`                            | Allowed host headers            |
| `CORS_ALLOW_ALL_ORIGINS` | Bool | `True`                                           | Allow all CORS origins          |
| `CORS_ALLOWED_ORIGINS` | CSV   | `http://localhost:3000,http://127.0.0.1:3000`    | Specific allowed CORS origins   |

---

## 📡 API Endpoints

### Base URL: `/api/v1/`

---

### 🔐 Auth — `/api/v1/users/`

| Method | Endpoint                        | Description                  | Auth |
|--------|---------------------------------|------------------------------|------|
| POST   | `/users/register/`              | Register a new user          | ❌   |
| POST   | `/users/login/`                 | Login & get JWT tokens       | ❌   |
| POST   | `/users/logout/`                | Blacklist refresh token      | ✅   |
| GET    | `/users/profile/`               | Get current user profile     | ✅   |
| PUT    | `/users/profile/`               | Update current user profile  | ✅   |
| POST   | `/users/password-reset/`        | Request password reset       | ❌   |
| POST   | `/users/password-reset/confirm/`| Confirm password reset       | ❌   |

---

### 📝 Posts — `/api/v1/posts/`

| Method | Endpoint              | Description                          | Auth       |
|--------|-----------------------|--------------------------------------|------------|
| GET    | `/posts/`             | List all published posts             | ❌         |
| GET    | `/posts/<id>/`        | Get post details (+increment view)   | ❌         |
| POST   | `/posts/`             | Create a new post                    | ✅         |
| PUT    | `/posts/<id>/`        | Update a post                        | ✅ Author  |
| PATCH  | `/posts/<id>/`        | Partial update a post                | ✅ Author  |
| DELETE | `/posts/<id>/`        | Delete a post                        | ✅ Author  |
| GET    | `/posts/categories/`  | List all categories                  | ❌         |
| POST   | `/posts/categories/`  | Create a category                    | ✅ Admin   |
| GET    | `/posts/tags/`        | List all tags                        | ❌         |
| POST   | `/posts/tags/`        | Create a tag                         | ✅ Admin   |
| GET    | `/posts/my/`          | List current user's posts            | ✅         |

---

### 💬 Comments — `/api/v1/comments/`

| Method | Endpoint               | Description                  | Auth       |
|--------|------------------------|------------------------------|------------|
| GET    | `/comments/?post=<id>` | List comments for a post     | ❌         |
| POST   | `/comments/`           | Create a new comment         | ✅         |
| GET    | `/comments/<id>/`      | Get comment details          | ❌         |
| PUT    | `/comments/<id>/`      | Update a comment             | ✅ Author  |
| DELETE | `/comments/<id>/`      | Delete a comment             | ✅ Author  |
| POST   | `/comments/like/`      | Toggle like on a post        | ✅         |
| GET    | `/comments/likes/?post=<id>` | List likes for a post  | ❌         |

---

### 📄 API Documentation

| Method | Endpoint         | Description                    |
|--------|------------------|--------------------------------|
| GET    | `/api/schema/`   | OpenAPI 3.0 schema (JSON/YAML) |
| GET    | `/api/docs/`     | Swagger UI                     |
| GET    | `/api/redoc/`    | ReDoc UI                       |

---

## 🔑 Authentication

This API uses **JWT (JSON Web Token)** authentication via `djangorestframework-simplejwt`.

- **Access Token Lifetime:** 60 minutes
- **Refresh Token Lifetime:** 7 days
- **Header Format:** `Authorization: Bearer <access_token>`

---

## 📊 Grading Criteria

| Category            | Points |
|---------------------|--------|
| Models              | 30     |
| Serializers         | 25     |
| Views               | 25     |
| Admin               | 10     |
| Custom Permission   | 5      |
| Code Quality        | 5      |
| **Total**           | **100**|

