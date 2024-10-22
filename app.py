from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {
        "id": 0,
        "title": "Harry Potter and the Philosopher's Stone",
        "author": "J.K. Rowling",
        "liked": True,
    },
    {
        "id": 1,
        "title": "Jurassic Park",
        "author": "Michael Crichton",
        "liked": False,
    },
    {
        "id": 2,
        "title": "The Hobbit",
        "author": "J.R.R. Tolkien",
        "liked": True,
    },
    {
        "id": 3,
        "title": "To Kill a Mocking Bird",
        "author": "Harper Lee",
        "liked": False,
    },
]

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/books")
async def read_books():
    return BOOKS

@app.get("/books/liked")
async def read_liked_books():
    return [book for book in BOOKS if book["liked"]]

# query parameter
@app.get("/books/")
async def read_books_by_author(author: str):
    return [book for book in BOOKS if book["author"].casefold() == author.casefold()]

# path parameter
@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int):
    return BOOKS[book_id]