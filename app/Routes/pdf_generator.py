import datetime
from time import timezone
import uuid
from fastapi import APIRouter, HTTPException, Body, Header, Depends, Request
from fastapi.responses import StreamingResponse, JSONResponse
from app.Utils.Danfe.danfe_utils import create_pdf
from app.Models.Danfe.models import Danfe
from app.Models.Errors.errors import custom_error_response

router = APIRouter()

header = {
    "tenantid": str,
    "username": str,
    "useremail": str
}

def verify_headers(
    tenantid: str = Header(None),
    username: str = Header(None),
    useremail: str = Header(None)
):
    errors = []

    if tenantid is None:
        errors.append({
            "code_error": "ORBIT_10001",
            "msg": "tenantid is required",
            "location": "header",
            "property_errors": [{
                "value": None,
                "type": "technical-error",
                "code_error": "ORBIT_10001",
                "msg": "tenantid is required",
                "property": "tenantid"
            }]
        })

    if username is None:
        errors.append({
            "code_error": "ORBIT_10002",
            "msg": "username is required",
            "location": "header",
            "property_errors": [{
                "value": None,
                "type": "technical-error",
                "code_error": "ORBIT_10002",
                "msg": "username is required",
                "property": "username"
            }]
        })

    if useremail is None:
        errors.append({
            "code_error": "ORBIT_10003",
            "msg": "useremail is required",
            "location": "header",
            "property_errors": [{
                "value": None,
                "type": "technical-error",
                "code_error": "ORBIT_10003",
                "msg": "useremail is required",
                "property": "useremail"
            }]
        })

    if errors:
        error_response = {
            "code": 400,
            "message": "Bad Request",
            "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
            "requestid": str(uuid.uuid4()),
            "errors": errors
        }
        raise HTTPException(status_code=400, detail=error_response)

    return {"tenantid": tenantid, "username": username, "useremail": useremail}

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
            code_error="PDF_B001",
            msg=e.detail,
            location="body"
        )
        return JSONResponse(status_code=e.status_code, content=error_response)
    except Exception as e:
        error_response = custom_error_response(
            code=500,
            message="Internal Server Error",
            code_error="PDF_B500",
            msg=str(e),
            location="server"
        )
        return JSONResponse(status_code=500, content=error_response)
