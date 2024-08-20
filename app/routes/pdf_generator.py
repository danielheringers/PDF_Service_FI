from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse, JSONResponse
from app.utils.danfe.danfe_utils import create_pdf
from app.models.danfe.models import Danfe
from app.models.Errors.errors import custom_error_response

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
    except HTTPException as e:
        error_response = custom_error_response(
            code=e.status_code,
            message="HTTP Error",
            code_error="ORBIT_10001",
            msg=e.detail,
            location="body"
        )
        return JSONResponse(status_code=e.status_code, content=error_response)
    except Exception as e:
        error_response = custom_error_response(
            code=500,
            message="Internal Server Error",
            code_error="ORBIT_50001",
            msg=str(e),
            location="server"
        )
        return JSONResponse(status_code=500, content=error_response)
