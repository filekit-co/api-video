import mimetypes
import urllib.parse
from enum import Enum, unique
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


@unique
class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
    
    @classmethod
    def choices(cls) -> tuple[str, ...]:
        return tuple(x.value for x in cls)
