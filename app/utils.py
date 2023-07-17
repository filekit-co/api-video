import mimetypes
import urllib.parse
from enum import Enum, unique
from functools import lru_cache
from typing import AsyncIterator

mimetypes.init()

_CHUNK_SIZE = 10 * 1024 * 1024 #10MB

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


# Chunk size 
async def generate_chunks(out_bytes, chunk_size=_CHUNK_SIZE)-> AsyncIterator[bytes]:
    index = 0
    while index < len(out_bytes):
        chunk = out_bytes[index : index + chunk_size]
        index += chunk_size
        yield chunk