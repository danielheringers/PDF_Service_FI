from typing import Any, List, Optional, Union

from fastapi import APIRouter, Body, Header, HTTPException, Response
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from threading import Lock
from app.api.auth_module.authorizer import Authorization
from app.modules.charges.bankslip.schemas import Boleto
from app.modules.charges.bankslip.service import create_pdf_boleto


boleto_router = APIRouter()
# reportlab_lock = Lock()
class ApiGatewayBody(BaseModel):
    body_json: Optional[List[Boleto]] = Field(None, alias="body-json")
    api_gateway_params: Any = Field(..., alias="api-gateway-params")

# def thread_safe_create_pdf(data):
#     with reportlab_lock:
#         return create_pdf_boleto(data)

@boleto_router.post("/boleto")
async def create_bankslip_pdf_endpoint(
    data: Union[ApiGatewayBody, List[Boleto]] = Body(...),
    tenantid: str = Header(...),
):

    if isinstance(data, ApiGatewayBody) and data.body_json:
        pdf_data = data.body_json
        api_gateway_params = data.api_gateway_params

        query = {
            "$and": ["fastpdf.bankslip.generate"],
            "active": True
        }

        if not api_gateway_params or "context" not in api_gateway_params:
            raise HTTPException(status_code=400, detail="Missing context in API Gateway parameters")
        elif not api_gateway_params["context"].get("authorizations"):
            raise HTTPException(status_code=401, detail="Unauthorized")

        auth_validator = await Authorization.create(query=query, request_headers=api_gateway_params["context"])
        auth_response = await auth_validator.validate()

        if auth_response["status"] == 401:
            raise HTTPException(status_code=401, detail=auth_response["body"])

    elif isinstance(data, list):
        pdf_data = data
    else:
        raise HTTPException(status_code=400, detail="Invalid request format")
    
    # pdf_buffer = await run_in_threadpool(thread_safe_create_pdf, pdf_data)
    pdf_buffer = create_pdf_boleto(pdf_data)
    pdf_buffer.seek(0)

    providerNumbers = [boleto.billing.billing_provider_number for boleto in pdf_data if hasattr(boleto, 'billing')]
    providerNumbers_str = "_".join(providerNumbers) if providerNumbers else "boleto"

    pdf_content = pdf_buffer.read()

    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename={providerNumbers_str}.pdf'}
    )
