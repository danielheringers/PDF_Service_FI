from typing import List
from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse
from app.schemas.boleto.models import Boleto
from app.services.boletos.boleto_render import create_pdf_boleto
from app.core.security import verify_headers

router = APIRouter()

@router.post("/pdf/boleto")
async def create_bankslip_pdf_endpoint(
    data: List[Boleto] = Body(...), 
    headers: dict = Depends(verify_headers)
):
    pdf_buffer = create_pdf_boleto(data)
    pdf_buffer.seek(0)
    erp_ids = [boleto.erp_id for boleto in data]
    erp_ids_str = "_".join(erp_ids)

    return StreamingResponse(
        pdf_buffer, 
        media_type='application/pdf', 
        headers={"Content-Disposition": f'inline; filename={erp_ids_str}.pdf'}
    )