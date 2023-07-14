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


ydl_opts = {
    'outtmpl': './downloads/%(id)s.%(extractor)s.%(ext)s',
    'quiet': True,
    # 'no_color': True,
    'noplaylist': True
}


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

    def get_info_sanitized(self, url):
        info = self.try_info(url)
        return self.sanitize_info(info)

    def get_filename(self, url):
        info = self.try_info(url)
        if info is None:
            return ""
        return f"{info['id']}.{info['extractor']}.{info['ext']}"

    def get_mp3_filename(self, url):
        info = self.try_info(url)
        if info is None:
            return ""
        return f"{info['id']}.{info['extractor']}.mp3"

    def try_download(self, url):
        try:
            return self.download([url])
        except:
            return -1

    def get_formats(self,url):
        info = self.get_info(url)
        formats = []
        if info is not None:
            for fmt in info['formats']:
                fi = FormatInfo.parse_obj(fmt)
                formats.append(fi)
            return formats
        else:
            return None

    def pick_format(self,format_id):
        self.format_selector = self.build_format_selector(format_id)

    def mp3_mode(self):
        self.add_post_processor(FFmpegExtractAudioPP(preferredcodec='mp3'))
