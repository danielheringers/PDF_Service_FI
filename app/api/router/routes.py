from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse
from app.schemas.danfe.models import Danfe
from app.schemas.boleto.models import Boleto
from app.services.danfe.danfe_utils import create_pdf_danfe
from app.services.boletos.boleto_render import create_pdf_boleto
from app.core.security import verify_headers
from app.services.boletosV2.boleto_render import create_pdf_teste

router = APIRouter()

@router.post("/gerar/pdf")
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

@router.post("/gerar/pdf/teste")
async def create_boleto_pdf_endpoint(

):
    pdf_buffer = create_pdf_teste()
    pdf_buffer.seek(0)
    return StreamingResponse(
        pdf_buffer, 
        media_type='application/pdf', 
        headers={"Content-Disposition": f'inline; filename=boleto.pdf'}
    )