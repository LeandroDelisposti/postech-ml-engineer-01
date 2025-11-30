import sys
from fastapi import FastAPI
import scraper
import uvicorn
import pandas as pd

print(".".join(map(str, sys.version_info[:3])))

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
    """
    /api/v1/scrape: inicia o processo de raspagem de dados.
    
    Returns:
        dict: A success message of the scraping process.
    """
    scraper.scrape_books()
    return {"message": "Scraping process triggered successfully."}

@app.get("/api/v1/books")
def get_all_books():
    """
    /api/v1/books: lista todos os livros disponíveis na base de dados.
    Returns:
        list[dict]: A list of book objects, where each object is a dictionary containing book details.
        dict: An error message if the 'books.csv' file is not found or another exception occurs during processing.
    """
    try:
        df = pd.read_csv("data/books.csv")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        return {"message": "books.csv not found. Please ensure data scraping has occurred."}
    except Exception as e:
        return {"message": f"An error occurred while reading books data: {str(e)}"}
    
    return df.to_dict(orient="records")

@app.get("/api/v1/books/search")
def search_books(title: str = "", category: str = ""):
    """
    /api/v1/books/search?title={title}&category={category}: 
    busca livros por título e/ou categoria.
    
    Args:
        title (str, optional): The title of the book to search for. Defaults to "".
        category (str, optional): The category of the book to search for. Defaults to "".
    
    Returns:
        list[dict]: A list of book objects, where each object is a dictionary containing book details.
        dict: An error message if the 'books.csv' file is not found or another exception occurs during processing.
    """
    try:
        df = pd.read_csv("data/books.csv")
        if title and category:
            filtered_books = df[(df["title"].str.contains(title, case=False)) & (df["category"] == category)].to_dict(orient="records")
        elif title:
            filtered_books = df[df["title"].str.contains(title, case=False)].to_dict(orient="records")
        elif category:
            filtered_books = df[df["category"] == category].to_dict(orient="records")
        else:
            filtered_books = df.to_dict(orient="records")
        return filtered_books
    except FileNotFoundError:
        return {"message": "books.csv not found. Please ensure data scraping has occurred."}
    except Exception as e:
        return {"message": f"An error occurred while searching books data: {str(e)}"}

@app.get("/api/v1/books/{id}")
def get_book_by_id(id: int):
    """
    /api/v1/books/{id}: retorna detalhes completos de um livro específico pelo ID.
    
    Args:
        id (int): The ID of the book to retrieve.
    
    Returns:
        dict: A dictionary containing book details.
        dict: An error message if the 'books.csv' file is not found or another exception occurs during processing.
    """
    try:
        df = pd.read_csv("data/books.csv")
        
        # get by line number
        book = df.iloc[id].to_dict()
        return book
    except FileNotFoundError:
        return {"message": "books.csv not found. Please ensure data scraping has occurred."}
    except Exception as e:
        return {"message": f"An error occurred while reading books data: {str(e)}"}

@app.get("/api/v1/categories")
def get_categories():
    """
    /api/v1/categories: lista todas as categorias de livros disponí veis.
    
    Returns:
        list[str]: A list of category names.
        dict: An error message if the 'books.csv' file is not found or another exception occurs during processing.
    """
    try:
        df = pd.read_csv("data/books.csv")
        categories = df["category"].unique().tolist()
        return {"categories": categories}
    except FileNotFoundError:
        return {"message": "books.csv not found. Please ensure data scraping has occurred."}
    except Exception as e:
        return {"message": f"An error occurred while reading categories data: {str(e)}"}

@app.get("/api/v1/health")
def health_check():
    """
    /api/v1/health: verifica status da API e conectividade com os dados.
    
    Returns:
        dict: A dictionary containing the status of the API.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)