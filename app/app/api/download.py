import logging

from fastapi import APIRouter, File, Query, Response, UploadFile, status
from infra.yt_downaloder import Downloader

router = APIRouter(prefix='/download')


@router.post(
        path="/mp3",
        tags=["Download to mp3"],
        summary="Download to mp3",
        description="Download to mp3",
    )
async def download_mp3(
        url: str = Query(
            default=..., description="Video URL"
        ),
    ):
    
    with Downloader() as ydl:
        filename = ydl.get_filename(url)
        ydl.mp3_mode()
        res = ydl.download([url])
        print(res)
        return filename
