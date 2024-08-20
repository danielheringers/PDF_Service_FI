from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.Routes.pdf_generator import router as pdf_generator_router
from app.Models.Errors.errors import custom_error_response

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    for error in errors:
        if error['loc'][0] == 'header':
            header_name = error['loc'][1]
            error_response = custom_error_response(
                code=400,
                message="Bad Request",
                code_error="ORBIT_10001",
                msg=f"{header_name} is required",
                location="header",
                property_name=header_name,
                value=None
            )
            return JSONResponse(status_code=400, content=error_response)
    return JSONResponse(status_code=422, content={"detail": errors})

app.include_router(pdf_generator_router)

