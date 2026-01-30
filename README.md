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

## 🧪 Testing

Run tests with:

```bash
python manage.py test
```

---

## 👤 Author

**Dmitriy Rebrykov**

---

## 📄 License

This project is distributed without a license (or specify the required license).

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Apply migrations

```bash
python manage.py migrate
```

### 3. Run the development server

```bash
python manage.py runserver
```

### 4. Open the API

**[http://localhost:8000/api/projects/](http://localhost:8000/api/projects/)**

---

## 📊 API Endpoints

### Projects

```
GET    /api/projects/                    → List projects
POST   /api/projects/                    → Create a project (with places)
GET    /api/projects/{id}/               → Retrieve a project
PATCH  /api/projects/{id}/               → Update a project
DELETE /api/projects/{id}/               → Delete a project
```

### Places

```
GET    /api/projects/{id}/places/                     → List places in a project
POST   /api/projects/{id}/places/add/                 → Add a place
GET    /api/projects/{id}/places/{place_id}/          → Retrieve a place
PATCH  /api/projects/{id}/places/{place_id}/update/   → Update a place
```

---

## 📑 API Documentation (Swagger)

Interactive API documentation is available via Swagger (OpenAPI):

* **Swagger UI**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
* **Redoc**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)

---

