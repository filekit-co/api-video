import mimetypes
import urllib.parse
from functools import lru_cache

mimetypes.init()

def content_disposition(filename):
    filename = urllib.parse.quote(filename)
    return f"attachment; filename*=UTF-8''{filename}"


@lru_cache
def get_mimetype(ext: str):
    """ext example .doc .docx"""
    return mimetypes.types_map.get(ext)

@lru_cache
def get_extension(mime_type: str, exclude_leading_dot=True):
    result = mimetypes.guess_extension(mime_type)
    
    if exclude_leading_dot:
        return result[1:]
    return result