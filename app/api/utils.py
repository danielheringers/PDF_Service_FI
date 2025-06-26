from fastapi import Header, HTTPException

def validate_accept_header(accept: str = Header(...)):
    if accept not in ("text/plain", "application/pdf"):
        raise HTTPException(status_code=406, detail="Not Acceptable: Only text/plain and application/pdf are allowed.")        
    return accept
