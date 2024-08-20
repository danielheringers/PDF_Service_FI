from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import pdf_generator
from app.models.Errors.errors import custom_error_response

app = FastAPI()

# Inclua o router
app.include_router(pdf_generator.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the PDF Generator API"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Captura o primeiro erro da lista de erros, você pode modificar isso para capturar todos
    first_error = exc.errors()[0]
    error_response = custom_error_response(
        code=400,
        message="Validation Error",
        code_error="VALIDATION_ERROR",  # Código de erro personalizado para validações
        msg=first_error['msg'],
        location=".".join(map(str, first_error['loc'])),
        property_name=first_error['loc'][-1],
        value=first_error['input']
    )
    return JSONResponse(status_code=400, content=error_response)
