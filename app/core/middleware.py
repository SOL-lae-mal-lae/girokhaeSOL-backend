from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.middleware("http")
async def wrap_response(request: Request, call_next):
    response = await call_next(request)
    
    # 이미 JSONResponse라면 body 꺼내오기
    if isinstance(response, JSONResponse):
        content = response.body
        # body가 bytes 이므로 decode 필요
        import json
        content_json = json.loads(content.decode())
    else:
        content_json = None

    wrapped = {
        "message": "Success",   # 필요하다면 커스텀 로직으로 message 채우기
        "data": content_json
    }

    return JSONResponse(content=wrapped)
