import io
from contextlib import redirect_stdout
from enum import Enum

from fastapi import APIRouter, HTTPException, Response
from infra.yt_downaloder import SUPPORTED_AUDIO_EXTS, AudioTypeEnum, Downloader
from utils import content_disposition, get_mimetype

from app.models import VideoInfo

router = APIRouter()

# https://github.com/yt-dlp/yt-dlp/issues/3298#issuecomment-1181754989
def download_audio(url: str, to_ext: str) -> bytes:
    with io.BytesIO() as buffer:
        with redirect_stdout(buffer), Downloader() as ydl:
            ydl.to_audio(to_ext)
            ydl.download([url])
            return buffer.getvalue()

@router.post(
        path="/download",
        tags=["Download to x"],
        summary="Download to x",
        description=f"audio x is types of {SUPPORTED_AUDIO_EXTS}",
    )
async def download(
        url: str,
        filename: str,
        to: AudioTypeEnum,
    ):
    if to in SUPPORTED_AUDIO_EXTS:
        out_bytes = download_audio(url, to)
    else:
        # TODO: not audio
        ...
    
    out_filename = f'{filename}.{to}'

    return Response(
        content=out_bytes,
        headers={
            'Content-Disposition': content_disposition(out_filename)
            },
        media_type=get_mimetype(f'.{to}'),
    )


@router.post("/info")
async def info(url: str):
    # filename = ydl.get_filename(url)
    
    with Downloader() as ydl:    
        info = ydl.get_info(url)

        if info is None:
            raise HTTPException(status_code=404, detail="URL not supported")
        else:
            return VideoInfo(
                title=info.get('title'),
                thumbUrl=info.get('thumbnail'),
                url=info.get('webpage_url')
            )
