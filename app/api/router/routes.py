from typing import List
from fastapi import APIRouter, Body, HTTPException, Header, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from app.schemas.boleto.models import Boleto
from app.services.boletos.boleto_render import create_pdf_boleto
# from app.services.danfe.danfe_utils import create_pdf_danfe
# from app.schemas.danfe.models import Danfe
from app.schemas.errors.custom_exception import HeaderMissingException

router = APIRouter()

def verify_headers(
    tenantid: str = Header(None),
):
    missing_headers = []
    if tenantid is None:
        missing_headers.append("tenantid")
        
    if missing_headers:
        raise HeaderMissingException(missing_headers)
    
    return {"tenantid": tenantid}

# @router.post("/gerar/pdf/danfe")
# async def create_danfe_pdf_endpoint(
#     data: Danfe = Body(...),
#     headers: dict = Depends(verify_headers)
# ):
#     pdf_buffer = create_pdf_danfe(data)
#     pdf_buffer.seek(0)
#     return StreamingResponse(
#         pdf_buffer, 
#         media_type='application/pdf', 
#         headers={"Content-Disposition": f'inline; filename={data.identificacao.codigoNf}.pdf'}
#     )
    
    
@router.post("/gerar/pdf/boleto")
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