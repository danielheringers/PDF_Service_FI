from fastapi import FastAPI
from app.routes import pdf_generator

app = FastAPI()

app.include_router(pdf_generator.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Generator API"}
