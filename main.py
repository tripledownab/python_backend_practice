from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import calculators

app = FastAPI()

origins = [
  "https://financeanalytica.io/",
  "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(calculators.router)
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(users.router)