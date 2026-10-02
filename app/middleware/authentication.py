from fastapi import Request
from fastapi.responses import JSONResponse
from app.storage import tokens

async def authentication_middleware(request: Request, call_next):
    token = request.headers.get("Authorization")

    if request.url.path.startswith("/todos"):
        if token not in tokens:
            return JSONResponse(status_code=401, content={"error": "Unauthorized"})
        request.state.user = tokens[token]

    response = await call_next(request)
    return response
