import os

mime_type_map = {
    ".html": b"text/html",
    ".htm": b"text/html",
    ".js": b"text/javascript",
    ".css": b"text/css",
    ".jpg": b"image/jpeg",
    ".jpeg": b"image/jpeg",
    ".png": b"image/png",
    ".gif": b"image/gif",
    ".ico": b"image/x-icon"
}


def get_mime_type(file_path: str) -> bytes:
    last_dot_index = file_path.rfind(".")
    mime_type = b"text/plain"
    if last_dot_index > -1:
        file_type = file_path[last_dot_index:]
        if file_type in mime_type_map:
            mime_type = mime_type_map[file_type]
    return mime_type
