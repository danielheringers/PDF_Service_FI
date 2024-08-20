import datetime
from time import timezone
import uuid
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.Routes.pdf_generator import router as pdf_generator_router
from app.Models.Errors.errors import custom_error_response
class HeaderMissingException(Exception):
    def __init__(self, missing_headers: list):
        self.missing_headers = missing_headers
        
app = FastAPI()

@app.exception_handler(HeaderMissingException)
async def header_missing_exception_handler(request: Request, exc: HeaderMissingException):
    errors = []
    for header in exc.missing_headers:
        errors.append({
            "code_error": f"PDF_H000{exc.missing_headers.index(header) + 1}",
            "msg": f"{header} is required",
            "location": "header",
            "property_errors": [{
                "value": None,
                "type": "technical-error",
                "code_error": f"PDF_H000{exc.missing_headers.index(header) + 1}",
                "msg": f"{header} is required",
                "property": header
            }]
        })
    
    response = {
        "code": 400,
        "message": "Bad Request",
        "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
        "requestid": str(uuid.uuid4()),
        "errors": errors
    }
    return JSONResponse(status_code=400, content=response)

app.include_router(pdf_generator_router)

