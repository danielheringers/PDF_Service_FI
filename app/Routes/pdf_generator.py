from fastapi import APIRouter, HTTPException, Body, Header, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.Utils.Danfe.danfe_utils import create_pdf
from app.Models.Danfe.models import Danfe
from app.Models.Errors.errors import custom_error_response
import uuid
from datetime import datetime

router = APIRouter()

def verify_headers(
    tenantid: str = Header(None),
    username: str = Header(None),
    useremail: str = Header(None)
):
    if tenantid is None:
        error_response = custom_error_response(
            code=400,
            message="Bad Request",
            code_error="ORBIT_10001",
            msg="tenantid is required",
            location="header",
            property_name="tenantid",
            value=None
        )
        raise HTTPException(status_code=400, detail=error_response["message"], headers=error_response)
    if username is None:
        error_response = custom_error_response(
            code=400,
            message="Bad Request",
            code_error="ORBIT_10002",
            msg="username is required",
            location="header",
            property_name="username",
            value=None
        )
        raise HTTPException(status_code=400, detail=error_response["message"], headers=error_response)
    if useremail is None:
        error_response = custom_error_response(
            code=400,
            message="Bad Request",
            code_error="ORBIT_10003",
            msg="useremail is required",
            location="header",
            property_name="useremail",
            value=None
        )
        raise HTTPException(status_code=400, detail=error_response["message"], headers=error_response)

    return {"tenantid": tenantid, "username": username, "useremail": useremail}

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
        return JSONResponse(status_code=e.status_code, content=e.headers)
    except Exception as e:
        error_response = custom_error_response(
            code=500,
            message="Internal Server Error",
            code_error="ORBIT_50001",
            msg=str(e),
            location="server"
        )
        return JSONResponse(status_code=500, content=error_response)
