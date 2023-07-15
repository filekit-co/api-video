import io
from enum import auto

from utils import StrEnum
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.ffmpeg import FFmpegExtractAudioPP


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


base_ydl_opts = {
    "outtmpl": "-",
    'logtostderr': True,
    'noplaylist': True,
    'quiet': True,
}


class Downloader(YoutubeDL):

    def __init__(self):
        super().__init__(base_ydl_opts)

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

    def to_audio(self, ext: str):
        self.add_post_processor(FFmpegExtractAudioPP(preferredcodec=ext))
