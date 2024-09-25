from fastapi import Header
from app.schemas.errors.custom_exception import HeaderMissingException

def verify_headers(
    tenantid: str = Header(None),
):
    missing_headers = []
    if tenantid is None:
        missing_headers.append("tenantid")
    
    if missing_headers:
        raise HeaderMissingException(missing_headers)
    
    return {"tenantid": tenantid}
