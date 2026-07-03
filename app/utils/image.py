import base64
import os
import uuid

UPLOAD_DIR = "assets/uploads/profiles"


def save_base64_image(base64_str: str) -> str:
    """Save a base64-encoded image to disk and return the public URL path."""
    if "," in base64_str:
        header, base64_str = base64_str.split(",", 1)

    ext = "png"
    if "image/jpeg" in header or "image/jpg" in header:
        ext = "jpg"
    elif "image/png" in header:
        ext = "png"
    elif "image/webp" in header:
        ext = "webp"
    elif "image/gif" in header:
        ext = "gif"

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(base64.b64decode(base64_str))

    return f"/{UPLOAD_DIR}/{filename}"
