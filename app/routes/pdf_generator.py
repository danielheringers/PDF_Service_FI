from fastapi import APIRouter, HTTPException, Body
from fastapi.responses import StreamingResponse
from app.utils.danfe.danfe_utils import create_pdf
from io import BytesIO

router = APIRouter()

@router.post("/generate-danfe-pdf")
def create_danfe_pdf_endpoint(data: dict = Body(...)):
    try:
        pdf_buffer = create_pdf(data)
        pdf_buffer.seek(0)
        return StreamingResponse(
            pdf_buffer, 
            media_type='application/pdf', 
            headers={"Content-Disposition": "inline; filename=document.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
