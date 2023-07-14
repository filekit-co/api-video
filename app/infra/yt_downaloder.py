import io

from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.ffmpeg import FFmpegExtractAudioPP

from app.models import FormatInfo


def process_hook_info(d):
    info={
        "status": d.get('status'),
        "downloaded_bytes": d.get('downloaded_bytes',0),
        "total_bytes": d.get('total_bytes',1),
        "filename": d.get('filename','.\\').split("\\")[-1],
    }
    return info


# ydl_opts = {
#     'outtmpl': './downloads/%(id)s.%(extractor)s.%(ext)s',
    # 'quiet': True,
#     # 'no_color': True,
#     'noplaylist': True
# }

ydl_opts = {
    "outtmpl": "-",
    'logtostderr': True,
    'noplaylist': True,
    # 'quiet': True,
}


SUPPORTED_AUDIO_EXTS = ['mp3', 'aac', 'm4a', 'opus', 'vorbis', 'flac', 'alac', 'wav']

class Downloader(YoutubeDL):

    def __init__(self):
        super().__init__(ydl_opts)

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
