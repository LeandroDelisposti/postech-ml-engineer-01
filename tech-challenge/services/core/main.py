from fastapi import FastAPI
import scraper

app = FastAPI(
    title="Book Recommendation - Core API",
    description="Core API for book data.",
    version="1.0.0",
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Core API"}

@app.post("/api/v1/scrape")
def trigger_scrape():
    scraper.scrape_books()
    return {"message": "Scraping process triggered successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

