from fastapi.responses import JSONResponse

def create_json_response(
    status_code: int = None, 
    message: str = None, 
    error_code: str = None, 
    data: str = None
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "message": message,
            "data": data,
            "error_code": error_code,
        },
        media_type="application/json",
    )