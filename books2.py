from fastapi import FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    suggested: bool = False
    
    def __init__(self, id: int, title: str, author: str, description: str, suggested: bool = False):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.suggested = suggested


ALLBOOKS = [Book(0, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", " ", True), 
            Book(1, "Jurassic Park", "Michael Crichton", " ", False),
            Book(2, "The Hobbit", "J.R.R. Tolkien", " ", True), 
            Book(3, "To Kill a Mocking Bird", "Harper Lee", " ", False),
            Book(4, "The Great Gatsby", "F. Scott Fitzgerald", " ", False), 
            Book(5, "The Catcher in the Rye", "J.D. Salinger", " ", False),
            Book(6, "1984", "George Orwell", " ", False), 
            Book(7, "The Da Vinci Code", "Dan Brown", " ", False),
                 ]

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/books")
async def read_books():
    return ALLBOOKS