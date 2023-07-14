
import logging
import os

import uvicorn
from fastapi import FastAPI, Request
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_utils.timing import add_timing_middleware

from app.api import download, greet

app = FastAPI(title='HDHA api server')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
add_timing_middleware(app, record=logging.error, prefix="app", exclude="untimed")

# TODO check (from fastapi.responses import FileResponse)
app.mount("/files", StaticFiles(directory="downloads"), name="downloads")

routers = [
    greet.router,
    download.router,
]

logger.error(routers)

for router in routers:
    app.include_router(router)


@app.middleware("http")
async def add_custom_header(request: Request, call_next):
    # after process
    response = await call_next(request)
    # 기존 응답 헤더에 'Access-Control-Expose-Headers' 헤더를 추가합니다.
    # CORS 정책으로 인해 Content-Disposition를 sveltekit이 못가져올 경우가 존재합니다.
    # Content-Disposition는 파일 이름을 전달하기 위해 필요합니다.
    response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), log_level="info")