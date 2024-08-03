from fastapi import FastAPI
from app.routes import pdf_generator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(pdf_generator.router)

origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origin=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Generator API"}
