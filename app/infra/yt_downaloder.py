import io
from contextlib import redirect_stdout
from enum import auto

from utils import StrEnum
from yt_dlp import YoutubeDL


class AudioTypeEnum(StrEnum):
    best = auto()
    mp3 = auto()
    aac = auto()
    m4a = auto()
    opus = auto()
    vorbis = auto()
    flac = auto()
    alac = auto()
    wav = auto()

SUPPORTED_AUDIO_EXTS = AudioTypeEnum.choices()


class VideoTypeEnum(StrEnum):
    avi = auto()
    flv = auto()
    mkv = auto()
    mov = auto()
    mp4 = auto()
    webm = auto()

SUPPORTED_VIDEO_EXTS = VideoTypeEnum.choices()


BASE_YDL_OPTS = {
    "outtmpl": "-", # for stream bytes download
    'logtostderr': True, # for stream bytes download
    'noplaylist': True,
    'playlist_items': '1:1',
    'concurrent_fragment_downloads': 5,
    'verbose': True,
}

# i.g filename = ydl.get_filename(url)
class Downloader(YoutubeDL):

    def __init__(self, opts=None):
        yd_opts = {**BASE_YDL_OPTS, **opts} if opts else BASE_YDL_OPTS
        super().__init__(yd_opts)

    def try_info(self, url):
        try:
            info = self.extract_info(url, download=False)
        except:
            return None
        return info

    def get_info(self, url):
        return self.try_info(url)

    def get_filename(self, url):
        info = self.try_info(url)
        if info is None:
            return ""
        return f"{info['id']}.{info['extractor']}.{info['ext']}"

# https://github.com/yt-dlp/yt-dlp/issues/3298#issuecomment-1181754989
async def download_audio(url: str, to_ext: AudioTypeEnum) -> bytes:
    audio_ydl_opts = {
    'format': f'm4a/bestaudio/best',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': to_ext,
    }]
    }

    with io.BytesIO() as buffer:
        with redirect_stdout(buffer), Downloader(audio_ydl_opts) as ydl:
            ydl.download([url])
            return buffer.getvalue()
        

async def download_video(url: str, to_ext: VideoTypeEnum, height: int) -> bytes:
    if height:
        video_ydl_opts = {
            # 'format': f'bv*[ext={to_ext}]+ba/bestvideo[ext=mp4]+bestaudio[ext=m4a] / bv*+ba/b',
            # 'format': f'bestvideo[ext={to_ext}][filesize<{MAX_FILESIZE}][height<={height}]+bestaudio/best[ext=mp4][filesize<{MAX_FILESIZE}]/best[filesize<{MAX_FILESIZE}]'
            # 'format': f'best[ext={to_ext}][filesize<{MAX_FILESIZE}][height<={height}]/bestvideo[ext=mp4]+bestaudio[ext=m4a][filesize<{MAX_FILESIZE}]'
            # 'format': f'best[ext={to_ext}][filesize<{MAX_FILESIZE}][height<={height}]'
            # f'bestvideo[ext={to_ext}][height<={height}]+bestaudio/best[height<={height}]'
            'format': f'best[ext={to_ext}][height<={height}]/best[ext=mp4]+bestaudio[ext=m4a]'
            # 'format': f'best[filesize<1K][res<{res+1}]+bestaudio/best'
            # 'format_sort': {'res': res, 'ext': to_ext}        
            # 'format': f'b[ext={to_ext}]',
            # 'format_sort': [f'height:{height}']
        }
    else:
        video_ydl_opts = { 
            'format': f'best[ext={to_ext}]/best[ext=mp4]+bestaudio[ext=m4a]'
        }

    with io.BytesIO() as buffer:
        with redirect_stdout(buffer), Downloader(video_ydl_opts) as ydl:
            ydl.download([url])
            return buffer.getvalue()
        