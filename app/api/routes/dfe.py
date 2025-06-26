import base64
from typing import List
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Response

from app.api.utils import validate_accept_header
from app.modules.dfes.damdfe.schemas import DamdfePayload
from app.modules.dfes.dacte.schemas import DactePayload
from app.modules.dfes.damdfe.service import generate_damdfe_pdf_bytes
from app.modules.dfes.dacte.service import generate_dacte_pdf_bytes

dfes_router = APIRouter()

@dfes_router.post("/mdfe/damdfe")
def generate_damdfe(
    data: DamdfePayload = Body(...),
    accept: str = Depends(validate_accept_header)
):
    pdf_data = data
    pdf_bytes = generate_damdfe_pdf_bytes(pdf_data)
    
    if accept == "text/plain":
        response_encoded = base64.b64encode(pdf_bytes.getvalue()).decode('utf-8')
        return response_encoded

    return Response(content=pdf_bytes.getvalue(), media_type="application/pdf")

@dfes_router.post("/cte/dacte")
def generate_damdfe(
    data: DactePayload = Body(...),
    accept: str = Depends(validate_accept_header)
):
    pdf_data = data
    pdf_bytes = generate_dacte_pdf_bytes(pdf_data)
    
    if accept == "text/plain":
        response_encoded = base64.b64encode(pdf_bytes.getvalue()).decode('utf-8')
        return response_encoded

    return Response(content=pdf_bytes.getvalue(), media_type="application/pdf")