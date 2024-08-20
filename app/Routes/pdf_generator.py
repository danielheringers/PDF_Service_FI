from fastapi import APIRouter, Body, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from app.Models.Errors.errors import custom_error_response
from app.Utils.Danfe.danfe_utils import create_pdf
from app.Models.Danfe.models import Danfe
from app.Models.Errors.custom_exception import HeaderMissingException

router = APIRouter()

def verify_headers(
    tenantid: str = Header(None),
    username: str = Header(None),
    useremail: str = Header(None)
):
    missing_headers = []
    if tenantid is None:
        missing_headers.append("tenantid")
    if username is None:
        missing_headers.append("username")
    if useremail is None:
        missing_headers.append("useremail")
    
    if missing_headers:
        raise HeaderMissingException(missing_headers)
    
    return {"tenantid": tenantid, "username": username, "useremail": useremail}

@router.post("/generate-danfe-pdf", status_code=201)
async def create_danfe_pdf_endpoint(
    data: Danfe = Body(...),
    headers: dict = Depends(verify_headers)
):
    pdf_buffer = create_pdf(data)
    pdf_buffer.seek(0)
    return StreamingResponse(
        pdf_buffer, 
        media_type='application/pdf', 
        headers={"Content-Disposition": "inline; filename=document.pdf"}
    )