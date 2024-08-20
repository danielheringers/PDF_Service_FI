from datetime import datetime, timedelta, timezone
import uuid

PST = timezone(timedelta(hours=-8))

def custom_error_response(code: int, message: str, code_error: str, msg: str, location: str, property_name: str = None, value=None):
    return {
        "code": code,
        "message": message,
        "timestamp": datetime.now(PST).isoformat(),
        "requestid": str(uuid.uuid4()),
        "errors": [
            {
                "code_error": code_error,
                "msg": msg,
                "location": location,
                "property_errors": [
                    {
                        "value": value,
                        "type": "technical-error",
                        "code_error": code_error,
                        "msg": msg,
                        "property": property_name,
                    }
                ]
            }
        ]
    }