from fastapi import Body, FastAPI, HTTPException
from pydantic import BaseModel

class BookInfo(BaseModel):
    id: int
    title: str
    author: str
    liked: bool

app = FastAPI()

ALLBOOKS = [
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
    return ALLBOOKS

# fixed path should be defined before the path with path parameter
@app.get("/books/liked")
async def read_liked_books():
    return [book for book in ALLBOOKS if book["liked"]]

# query parameter
@app.get("/books/")
async def read_books_by_author(author: str):
    return [book for book in ALLBOOKS if book["author"].casefold() == author.casefold()]

# path parameter
@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int):
    for book in ALLBOOKS:
      if book["id"] == book_id:
        return book
    return {"error": "Book not found"}

@app.post("/books/create_book")
async def create_book(post_book_infos: dict = Body(...)):
  new_id = max(book["id"] for book in ALLBOOKS) + 1 if ALLBOOKS else 0
  new_book = {
    "id": new_id,
    "title": post_book_infos["title"],
    "author": post_book_infos["author"],
    "liked": False,
  }
  ALLBOOKS.append(new_book)
  return new_book

@app.put("/books/{book_id}")
async def update_book(book_id: int, put_book_infos: BookInfo = Body(...)):
  for book in ALLBOOKS:
    if book["id"] == book_id:
      book["title"] = put_book_infos["title"]
      book["author"] = put_book_infos["author"]
      return {"info": "Book updated successfully", "data":book}
  raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
  for book in ALLBOOKS:
    if book["id"] == book_id:
      ALLBOOKS.remove(book)
      return # a successful deletion usually returns 204 No Content
  raise HTTPException(status_code=404, detail="Book not found")
