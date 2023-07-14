import io
import logging
from contextlib import redirect_stdout
from enum import Enum

from fastapi import APIRouter, File, Query, Response, UploadFile, status
from infra.yt_downaloder import Downloader
from utils import content_disposition, get_mimetype

router = APIRouter(prefix='/download')

# https://github.com/yt-dlp/yt-dlp/issues/3298#issuecomment-1181754989
def download(url: str) -> bytes:
    # filename = ydl.get_filename(url)
    with io.BytesIO() as buffer:
        with redirect_stdout(buffer), Downloader() as ydl:
            filename = ydl.get_filename(url)
            ydl.mp3_mode()
            ydl.download([url])
            return filename, buffer.getvalue()
    

class DownloadType(str, Enum):
    mp3 = "mp3"
    mp4 = "mp4"
    webm = "webm"



@router.post(
        path="/",
        tags=["Download to x"],
        summary="Download to x",
        description="Download to x",
    )
async def download(
        url: str,
        to: DownloadType,
    ):

    # TODO: out file format
    filename, mp3_bytes = download(url)
    return Response(
        content=mp3_bytes,
        headers={
            'Content-Disposition': content_disposition(filename)
            },
        media_type=get_mimetype('.mp3'),
    )
