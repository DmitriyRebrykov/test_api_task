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

## API Endpoints

### Travel Projects

#### 1. Create project
**POST** `/api/projects/`

**Request Body:**
```json
{
    "name": "European Art Tour",
    "description": "Tour of European art museums",
    "start_date": "2024-06-01",
    "places": [
        {
            "external_id": 27992,
            "notes": "Must see this masterpiece"
        },
        {
            "external_id": 28560,
            "notes": "Beautiful landscape"
        }
    ]
}
```

**Notes:**
- `description` и `start_date` optional
- `places` optional (you can create a project without locations)
- Minimum 1, maximum 10 seats
- `external_id` must exist in the Art Institute of Chicago API

**Response:** `201 Created`
```json
{
    "id": 1,
    "name": "European Art Tour",
    "description": "Tour of European art museums",
    "start_date": "2024-06-01",
    "places": [
        {
            "id": 1,
            "external_id": 27992,
            "title": "A Sunday on La Grande Jatte",
            "artist_display": "Georges Seurat",
            "date_display": "1884-86",
            "place_of_origin": "France",
            "artwork_type": "Painting",
            "image_id": "abc123",
            "notes": "Must see this masterpiece",
            "is_visited": false,
            "created_at": "2024-01-30T10:00:00Z",
            "updated_at": "2024-01-30T10:00:00Z"
        }
    ],
    "is_completed": false,
    "created_at": "2024-01-30T10:00:00Z",
    "updated_at": "2024-01-30T10:00:00Z"
}
```

#### 2. List of all projects
**GET** `/api/projects/`

**Response:** `200 OK`
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "European Art Tour",
            "description": "Tour of European art museums",
            "start_date": "2024-06-01",
            "places_count": 2,
            "is_completed": false,
            "created_at": "2024-01-30T10:00:00Z",
            "updated_at": "2024-01-30T10:00:00Z"
        }
    ]
}
```

#### 3. Obtain a specific project
**GET** `/api/projects/{id}/`

**Response:** `200 OK`
```json
{
    "id": 1,
    "name": "European Art Tour",
    "description": "Tour of European art museums",
    "start_date": "2024-06-01",
    "places": [...],
    "is_completed": false,
    "created_at": "2024-01-30T10:00:00Z",
    "updated_at": "2024-01-30T10:00:00Z"
}
```

#### 4. Update project
**PUT/PATCH** `/api/projects/{id}/`

**Request Body:**
```json
{
    "name": "Updated Project Name",
    "description": "Updated description",
    "start_date": "2024-07-01"
}
```

**Response:** `200 OK`

#### 5. Delete project
**DELETE** `/api/projects/{id}/`

**Notes:**
- Проект нельзя удалить, если хотя бы одно место отмечено как посещённое

**Response:** `204 No Content` или `400 Bad Request`
```json
{
    "error": "Cannot delete project with visited places",
    "detail": "A project cannot be deleted if any of its places are marked as visited"
}
```

### Places

#### 6. List of locations in the project
**GET** `/api/projects/{project_id}/places/`

**Response:** `200 OK`
```json
[
    {
        "id": 1,
        "external_id": 27992,
        "title": "A Sunday on La Grande Jatte",
        "artist_display": "Georges Seurat",
        "date_display": "1884-86",
        "place_of_origin": "France",
        "artwork_type": "Painting",
        "image_id": "abc123",
        "notes": "Must see this masterpiece",
        "is_visited": false,
        "created_at": "2024-01-30T10:00:00Z",
        "updated_at": "2024-01-30T10:00:00Z"
    }
]
```

#### 7. Get a specific place in the project
**GET** `/api/projects/{project_id}/places/{place_id}/`

**Response:** `200 OK`

#### 8. Add a location to an existing project
**POST** `/api/projects/{project_id}/places/add/`

**Request Body:**
```json
{
    "external_id": 28560,
    "notes": "Optional notes about this place"
}
```

**Notes:**
- `external_id` Must exist in the Art Institute of Chicago API
- Project cannot contain more than 10 locations
- The same location cannot be added twice to a single project

**Response:** `201 Created`

#### 9. Update location in project
**PATCH/PUT** `/api/projects/{project_id}/places/{place_id}/update/`

**Request Body:**
```json
{
    "notes": "Updated notes",
    "is_visited": true
}
```
---
