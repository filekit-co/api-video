import logging
from typing import Optional

import yt_dlp
from fastapi import APIRouter, HTTPException, Response
from infra.yt_downaloder import (SUPPORTED_AUDIO_EXTS, SUPPORTED_VIDEO_EXTS,
                                 AudioTypeEnum, Downloader, VideoTypeEnum,
                                 download_audio, download_video)
from utils import content_disposition, get_mimetype

from app.models import VideoInfo

router = APIRouter()

@router.post(
        path="/info",
        tags=["Download"],
        summary="Download target url info",
        )
async def info(url: str):
    with Downloader() as ydl:    
        info = ydl.get_info(url)
        logging.error(info)
        if info is None:
            raise HTTPException(status_code=400, detail="URL not supported")
        else:
            return VideoInfo(
                title=info.get('title'),
                thumbUrl=info.get('thumbnail'),
                url=info.get('webpage_url'),
                filesize_approx=info.get('filesize_approx'),

            )


@router.post(
        path="/download/audio",
        tags=["Download"],
        summary="Download to audio x",
        description=f"audio x is types of {SUPPORTED_AUDIO_EXTS}",
    )
async def audio(
        url: str,
        filename: str,
        to: AudioTypeEnum,
    ):
    if to in SUPPORTED_AUDIO_EXTS:
        out_bytes = download_audio(url, to)
    else:
        raise HTTPException(status_code=400, detail=f"{to} is not supported")
    
    out_filename = f'{filename}.{to}'

    return Response(
        content=out_bytes,
        headers={
            'Content-Disposition': content_disposition(out_filename)
            },
        media_type=get_mimetype(f'.{to}'),
    )


@router.post(
        path="/download/video",
        tags=["Download"],
        summary="Download to video",
        description=f"video x is types of {SUPPORTED_VIDEO_EXTS}",
    )
async def video(
        url: str,
        filename: str,
        to: VideoTypeEnum,
        height: Optional[int]=None,
    ):

    try:
        if to in SUPPORTED_VIDEO_EXTS:
            out_bytes = download_video(url, to, height)
        else:
            raise HTTPException(status_code=400, detail=f"{to} is not supported")
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=500, detail=e.msg)

    
    out_filename = f'{filename}.{to}'

    return Response(
        content=out_bytes,
        headers={
            'Content-Disposition': content_disposition(out_filename)
            },
        media_type=get_mimetype(f'.{to}'),
    )
