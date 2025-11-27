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

## Installation and Setup

1. **Clone the repository:** 
   ```bash
   git clone <repository-url>
   ```
2. **Install dependencies for each service:**
   - **Core Service:**
     ```bash
     pip install -r services/core/requirements.txt
     ```
   - **Insights Service:**
     ```bash
     pip install -r services/insights/requirements.txt
     ```
   - **Auth Service:**
     ```bash
     pip install -r services/auth/requirements.txt
     ```
   - **ML Service:**
     ```bash
     pip install -r services/ml/requirements.txt
     ```

## API Documentation (Swagger)

Each service has its own API documentation available at `/docs` when running.

- **Core Service:** `http://127.0.0.1:8001/docs`
- **Insights Service:** `http://127.0.0.1:8002/docs`
- **Auth Service:** `http://127.0.0.1:8003/docs`
- **ML Service:** `http://127.0.0.1:8004/docs`

## How to Run

- **Run the scraper:**
  ```bash
  python scripts/scraper.py
  ```
- **Run each service (in separate terminals):**
  - **Core Service:**
    ```bash
    uvicorn services.core.main:app --reload --port 8001
    ```
  - **Insights Service:**
    ```bash
    uvicorn services.insights.main:app --reload --port 8002
    ```
  - **Auth Service:**
    ```bash
    uvicorn services.auth.main:app --reload --port 8003
    ```
  - **ML Service:**
    ```bash
    uvicorn services.ml.main:app --reload --port 8004
    ```
- **Run tests:**
  ```bash
  pytest
  ```
