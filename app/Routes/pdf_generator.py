from fastapi import APIRouter, HTTPException, Body, Header, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from app.Utils.Danfe.danfe_utils import create_pdf
from app.Models.Danfe.models import Danfe
from app.Models.Errors.errors import custom_error_response

router = APIRouter()

def verify_headers(
    tenantid: str = Header(...),
    username: str = Header(...),
    useremail: str = Header(...)
):
    if not tenantid or not username or not useremail:
        raise HTTPException(
            status_code=400,
            detail="Missing required headers: tenantid, username, or useremail"
        )
    else:
        pass

@router.post("/generate-danfe-pdf")
def create_danfe_pdf_endpoint(
    data: Danfe = Body(...),
    headers: dict = Depends(verify_headers)
):
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
