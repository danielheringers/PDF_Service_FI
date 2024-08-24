from fastapi import Header
from app.schemas.errors.custom_exception import HeaderMissingException

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
