from fastapi import FastAPI

app = FastAPI(
    title="Book Recommendation - ML API",
    description="API for serving machine learning models and predictions.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML API"}

# TODO: Add the ML endpoints here
