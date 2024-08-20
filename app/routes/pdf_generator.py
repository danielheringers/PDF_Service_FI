from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse, JSONResponse
from io import BytesIO
from app.utils.danfe.danfe_utils import create_pdf
from app.models.danfe.models import Danfe
from datetime import datetime
from models.Errors.errors import custom_error_response

router = APIRouter()

@router.post("/generate-danfe-pdf")
def create_danfe_pdf_endpoint(data: Danfe = Body(...)):
    try:
        pdf_buffer = create_pdf(data)
        pdf_buffer.seek(0)
        return StreamingResponse(
            pdf_buffer, 
            media_type='application/pdf', 
            headers={"Content-Disposition": "inline; filename=document.pdf"}
        )
    except ValueError as e:
        error_response = custom_error_response(
            code=400,
            message="Bad Request",
            code_error="PDF_001",
            msg=str(e),
            location="body",
            property_name="Danfe"
        )
        return JSONResponse(status_code=400, content=error_response)
    except Exception as e:
        error_response = custom_error_response(
            code=500,
            message="Internal Server Error",
            code_error="PDF_50001",
            msg="An unexpected error occurred",
            location="server"
        )
        return JSONResponse(status_code=500, content=error_response)
