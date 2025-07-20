# E-commerce FastAPI

A production-ready E-commerce api built with FastAPI, MongoDB, and modern Python tooling.

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [MongoDB Models](#mongodb-models)
- [API Endpoints](#api-endpoints)
- [Production-Ready Practices](#production-ready-practices)

---

## Project Overview

This project provides a RESTful API for an E-commerce platform, supporting user authentication, product management, order processing, and more. It is designed for scalability, maintainability, and security.

## Technologies Used

- **FastAPI**: High-performance Python web framework
- **MongoDB**: NoSQL database for flexible data storage
- **Pymongo**: Async MongoDB driver for Python
- **Mongoengine**: A Object Document Mapper (ODM) for MongoDB
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for running FastAPI
- **Docker**: Containerization for deployment
- **Docker Compose**: Multi-container Docker application management
- **Render**: Cloud platform for deploying web applications

## Project Structure

```
E-commerce-fastapi/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── logging.py
│   ├── db.py
│   ├── models/
│   ├── routes/
│   ├── schemas/
|── logs/
│   ├── app.log
│   └── error.log
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
├── docker-compose.yaml
├── render.yaml
├── .dockerignore
└── README.md
```

- `app/models/`: MongoDB models and ODM definitions
- `app/routes/`: API route handlers
- `app/schemas/`: Pydantic schemas for request/response validation

## Getting Started

### Prerequisites

- Python 3.11 or higher
- MongoDB (local or cloud)
- Docker (optional)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/KanishkRastogi46/e-comm-fastapi.git
    cd e-comm-fastapi
    ```
2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set environment variables:**
    - Create a `.env` file with MongoDB URI

5. **Run the application:**
    ```bash
    uvicorn src.main:app --reload
    ```

6. **(Optional) Run with Docker:**
    ```bash
    docker build -t ecommerce-fastapi .
    docker run -d -p 8000:8000 --env-file .env ecommerce-fastapi
    ```
7. **(Optional) Start the mongodb service:**
    ```bash
    docker-compose -f docker-compose.yaml up -d
    ```

8. **Access the API:**
    - Open your browser and go to `http://localhost:8000/docs` to view the Swagger UI for API documentation. 
    - Alternatively, you can use tools like Postman or curl to interact with the API endpoints.

    ### _**Note**_: 
    After starting the application a logs folder will be created in the root directory. This folder contains structured logs for monitoring and debugging purposes.

## MongoDB Models

- **Products**
  - `id`, `name`, `price`, `sizes`, `created_at`, `updated_at`
- **Orders**
  - `id`, `userId`, `items`, `created_at`, `updated_at`


## API Endpoints

| Method | Endpoint             | Description                |
|--------|----------------------|----------------------------|
| GET    | `/products/`         | List all products          |
| POST   | `/products/`         | Create a new product       |
| GET    | `/orders/{userId}`   | List user orders           |
| POST   | `/orders/`           | Create a new order         |

## Production-Ready Practices

- **Environment Variables**: Sensitive data managed via `.env`
- **Async I/O**: Non-blocking database and API operations
- **Input Validation**: Pydantic schemas for all endpoints
- **Error Handling**: Consistent and informative error responses
- **Dockerization**: Easy deployment with Docker
- **Logging**: Structured logging for monitoring

---

Feel free to contribute or raise issues!