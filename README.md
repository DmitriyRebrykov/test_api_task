# Django REST API Project

## 📌 Description

A fully functional RESTful API for managing travel projects on Django REST Framework.

The project includes:

* RESTful endpoints
* Swagger / OpenAPI documentation
* Environment variable support

---

## 🛠️ Technology Stack

* Python 3.10+
* Django
* Django REST Framework
* drf-spectacular (Swagger / OpenAPI)
* SQLite 

---

## 📂 Project Structure

```text
.
├── apps/
│   └── projects/        # Main application with business logic
├── config/              # Django configuration (settings, urls, wsgi, asgi)
├── manage.py
├── requirements.txt
├── .env.example         # Environment variables example
└── README.md
```

---

## ⚙️ Installation and Setup

### 1️⃣ Clone the repository

```bash
git clone <repository_url>
cd test_api_task
```

---

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux / macOS
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure environment variables

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Fill in the required values (SECRET_KEY, DEBUG, DATABASE_URL, etc.).

---

### 5️⃣ Apply migrations

```bash
python manage.py migrate
```

---

### 6️⃣ Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```

---

## 📑 API Documentation (Swagger)

Swagger (OpenAPI) is enabled in the project.

### Available endpoints:

* **Swagger UI**:

  ```
  http://127.0.0.1:8000/api/docs/
  ```

* **Redoc**:

  ```
  http://127.0.0.1:8000/api/redoc/
  ```

* **OpenAPI Schema (JSON)**:

  ```
  http://127.0.0.1:8000/api/schema/
  ```

---

## 🔗 API Endpoints

The main endpoints are located in the following app:

```
apps/projects/
```

Examples:

| Method | URL                 | Description            |
| ------ | ------------------- | ---------------------- |
| GET    | /api/projects/      | Get a list of projects |
| POST   | /api/projects/      | Create a project       |
| GET    | /api/projects/{id}/ | Retrieve a project     |
| PUT    | /api/projects/{id}/ | Update a project       |
| DELETE | /api/projects/{id}/ | Delete a project       |

(See Swagger for the full and up-to-date list of endpoints.)

---
