from fastapi import FastAPI

app = FastAPI(
    title="Book Recommendation - Insights API",
    description="API for book data statistics and insights.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Insights API"}
