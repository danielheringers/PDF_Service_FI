from fastapi import APIRouter

from app.api.routes.charges import boleto_router
from app.api.routes.dfe import dfes_router

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"healthy": True}
    
router.include_router(boleto_router, prefix="/charges")
router.include_router(dfes_router, prefix="/dfes")