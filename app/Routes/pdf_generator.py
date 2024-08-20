from fastapi import APIRouter, Body, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from app.Models.Boleto.models import Boleto
from app.Utils.Boleto.boleto_render import create_pdf_boleto
from app.Utils.Danfe.danfe_utils import create_pdf_danfe
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

@router.post("/gerar/pdf/danfe")
async def create_danfe_pdf_endpoint(
    data: Danfe = Body(...),
    headers: dict = Depends(verify_headers)
):
    pdf_buffer = create_pdf_danfe(data)
    pdf_buffer.seek(0)
    return StreamingResponse(
        pdf_buffer, 
        media_type='application/pdf', 
        headers={"Content-Disposition": f'inline; filename={data.identificacao.codigoNf}.pdf'}
    )
    
    
@router.post("/gerar/pdf/boleto")
async def create_danfe_pdf_endpoint(
    data: Boleto = Body(...),
    headers: dict = Depends(verify_headers)
):
    pdf_buffer = create_pdf_boleto(data)
    pdf_buffer.seek(0)
    return StreamingResponse(
        pdf_buffer, 
        media_type='application/pdf', 
        headers={"Content-Disposition": f'inline; filename={data.erp_id}.pdf'}
    )