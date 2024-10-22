from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    suggested: bool = False
    
    def __init__(self, id: int, title: str, author: str, description: str, rating: int, suggested: bool = False):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.suggested = suggested

class BookRequest(BaseModel):
  id: Optional[int] = Field(description='ID is not needed for creating', default=None) # so create and update can be used interchangeably
  title: str = Field(min_length=1, max_length=100)
  author: str = Field(min_length=1, max_length=100)
  description: str = Field(min_length=1, max_length=200)
  rating: int = Field(ge=1, le=5)
  suggested: bool = False
  
  model_config = {
    "json_schema_extra": {
      "example": {
        "title": "Brand New Book",
        "author": "Definitely New Author",
        "description": "A Book that just pubhlished literally 1 second ago.",
        "rating": 5,
        "suggested": True
      }
    }
  }
    

ALLBOOKS = [
  Book(0, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", "A young wizard's journey begins.", 5, True),
  Book(1, "Jurassic Park", "Michael Crichton", "Dinosaurs are brought back to life with disastrous consequences.", 4, False),
  Book(2, "The Hobbit", "J.R.R. Tolkien", "A hobbit's adventure to reclaim a lost kingdom.", 5, True),
  Book(3, "To Kill a Mocking Bird", "Harper Lee", "A story of racial injustice in the Deep South.", 5, False),
  Book(4, "The Great Gatsby", "F. Scott Fitzgerald", "A critique of the American Dream in the Jazz Age.", 4, False),
  Book(5, "The Catcher in the Rye", "J.D. Salinger", "A teenager's experiences in New York City.", 3, False),
  Book(6, "1984", "George Orwell", "A dystopian future under totalitarian rule.", 5, False),
  Book(7, "The Da Vinci Code", "Dan Brown", "A symbologist uncovers a religious mystery.", 4, False),
]

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_books():
    return ALLBOOKS
  
@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(ge=0)):
    for book in ALLBOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found") # Error Handling
  
@app.get("/books_by_rating", status_code=status.HTTP_200_OK)
async def read_books_by_rating(rating: int = Query(ge=1, le=5)): 
    return [book for book in ALLBOOKS if book.rating == rating]
  
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book.id = generate_book_id()
    ALLBOOKS.append(new_book)
    return ALLBOOKS
  
@app.put("/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest):
  book_changed = False
  for book in ALLBOOKS:
      if book.id == book_request.id:
          book.title = book_request.title
          book.author = book_request.author
          book.description = book_request.description
          book.rating = book_request.rating
          book.suggested = book_request.suggested
          book_changed = True
  if not book_changed:
      raise HTTPException(status_code=404, detail="Book not found")
  
def generate_book_id():
    new_id = max([book.id for book in ALLBOOKS]) + 1 if ALLBOOKS else 0
    return new_id