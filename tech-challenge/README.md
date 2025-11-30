# Project Name: Book Recommendation API

## Description

This project is a complete data pipeline and public API for book data, extracted from https://books.toscrape.com/. The goal is to provide a clean and structured dataset for data scientists and machine learning services to build book recommendation systems.

## Architecture

This project is structured as a microservices application, with each service running independently.

- **Core Service:** Handles the main book data access.
- **Insights Service:** Provides statistical analysis of the book data.
- **Auth Service:** Manages user authentication and authorization.
- **ML Service:** Serves machine learning models and predictions.

See `docs/architecture.md` for the full architectural plan.

## Backlog

### Core Service
- Isolate core/scraper.py from core/__main__.py to have it's own pipeline
- Protect scraper.py with authentication (user: user, password: password)
- Implement JWT authentication

### Insights Service
- Implement a dashboard to show book data statistics
- Implement a dashboard to show book data visualizations
- Implement JWT authentication

### Auth Service
- Implement JWT authentication

### ML Service
- Implement a book recommendation system
- Implement JWT authentication

## Installation and Setup

1. **Clone the repository:** 
   ```bash
   git clone <repository-url>
   ```
2. **Install dependencies for each service:**
   ```bash
   uv pip install -r services/core/requirements.txt
   ```
   - **Insights Service:**
     ```bash
     uv pip install -r services/insights/requirements.txt
     ```
   - **Auth Service:**
     ```bash
     uv pip install -r services/auth/requirements.txt
     ```
   - **ML Service:**
     ```bash
     uv pip install -r services/ml/requirements.txt
       ```

## API Documentation (Swagger)

Each service has its own API documentation available at `/docs` when running.

- **Core Service:** `http://127.0.0.1:8000/docs`
- **Insights Service:** `http://127.0.0.1:8001/docs`
- **Auth Service:** `http://127.0.0.1:8002/docs`
- **ML Service:** `http://127.0.0.1:8003/docs`
## How to Run

- **Run the scraper:**
  ```bash
  python scripts/scraper.py
  ```
- **Run each service (in separate terminals):**
  - **Core Service:**
    ```bash
    cd services/core
    uv run uvicorn __main__.py --reload --port 8000
    ```
  - **Insights Service:**
    ```bash
    cd services/insights
    uv run uvicorn __main__.py --reload --port 8001
    ```
  - **Auth Service:**
    ```bash
    cd services/auth
    uv run uvicorn __main__.py --reload --port 8002
    ```
  - **ML Service:**
    ```bash
    cd services/ml
    uv run uvicorn __main__.py --reload --port 8003
    ```
- **Run tests:**
  ```bash
  uv run pytest
  ```
