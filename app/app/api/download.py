import io
from contextlib import redirect_stdout
from enum import Enum

from fastapi import APIRouter, HTTPException, Response
from infra.yt_downaloder import Downloader
from utils import content_disposition, get_mimetype

from app.models import VideoInfo

router = APIRouter()

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


@router.post("/info")
async def info(url: str):
    with Downloader() as ydl:
        info = ydl.get_info(url)

        if info is None:
            raise HTTPException(status_code=404, detail="URL not supported")
        else:
            return VideoInfo(
                title=info.get('title'),
                thumbUrl=info.get('thumbnail'),
                site=info.get('webpage_url_domain'),
                url=info.get('webpage_url')
            )
