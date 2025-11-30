from fastapi import FastAPI

app = FastAPI(
    title="Book Recommendation - Auth API",
    description="API for user authentication and authorization.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Auth API"}
