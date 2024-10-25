from fastapi import FastAPI
from routers import calculators

app = FastAPI()

app.include_router(calculators.router)
# app.include_router(auth.router)
# app.include_router(admin.router)
# app.include_router(users.router)