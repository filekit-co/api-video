from typing import Optional

import yt_dlp
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from infra.yt_downaloder import (SUPPORTED_AUDIO_EXTS, SUPPORTED_VIDEO_EXTS,
                                 AudioTypeEnum, Downloader, VideoTypeEnum,
                                 download_audio, download_video)
from pydantic import BaseModel
from utils import content_disposition, generate_chunks, get_mimetype

from app.models import VideoInfo

router = APIRouter()

class InfoRequest(BaseModel):
    url: str


@router.post(
        path="/info",
        tags=["Download"],
        summary="Download target url info",
        )
async def info(info_in: InfoRequest):
    with Downloader() as ydl:    
        info = ydl.get_info(info_in.url)
        if info is None:
            raise HTTPException(status_code=400, detail="URL not supported")
        else:
            return VideoInfo(
                title=info.get('title'),
                thumbUrl=info.get('thumbnail'),
                url=info.get('webpage_url'),
                filesize_approx=info.get('filesize_approx'),

            )


class AudioRequest(BaseModel):
    url: str
    filename: str
    to: AudioTypeEnum

@router.post(
        path="/download/audio",
        tags=["Download"],
        summary="Download to audio x",
        description=f"audio x is types of {SUPPORTED_AUDIO_EXTS}",
    )
async def audio(audio_in:AudioRequest):
    if audio_in.to not in SUPPORTED_AUDIO_EXTS:
        raise HTTPException(status_code=400, detail=f"{audio_in.to} is not supported")
    
    out_filename = f'{audio_in.filename}.{audio_in.to}'
    out_bytes = await download_audio(audio_in.url, audio_in.to)
    return StreamingResponse(
        content=generate_chunks(out_bytes),
        headers={
            'Content-Disposition': content_disposition(out_filename)
            },
        media_type=get_mimetype(f'.{audio_in.to}'),
    )

class VideoRequest(BaseModel):
    url: str
    filename: str
    to: VideoTypeEnum
    height: Optional[int]=None

@router.post(
        path="/download/video",
        tags=["Download"],
        summary="Download to video",
        description=f"video x is types of {SUPPORTED_VIDEO_EXTS}",
    )
async def video(
        video_in: VideoRequest
    ):
    try:
        if video_in.to not in SUPPORTED_VIDEO_EXTS:
            raise HTTPException(status_code=400, detail=f"{video_in.to} is not supported")

        out_filename = f'{video_in.filename}.{video_in.to}'
        out_bytes: bytes = await download_video(video_in.url, video_in.to, video_in.height)
        return StreamingResponse(
            content=generate_chunks(out_bytes),
            headers={
                'Content-Disposition': content_disposition(out_filename)
                },
            media_type=get_mimetype(f'.{video_in.to}'),
        )
    except yt_dlp.utils.DownloadError as e:
        raise HTTPException(status_code=500, detail=e.msg)
