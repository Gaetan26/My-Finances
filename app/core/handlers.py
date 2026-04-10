
from main import app
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code = exc.status_code,
        content = {
            "success": False,
            "content": {
                "error": exc.detail 
            }
        },
    )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code = 422,
        content = {
            "success": False,
            "content": {
                "error": exc.errors()
            }
        },
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "content": {
                "error": "Internal Server Error",
                "more": str(exc)  # for dev only
            },
        },
    )
