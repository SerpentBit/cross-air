from mimetypes import MimeTypes
from pathlib import PurePath

from fastapi import UploadFile, HTTPException

IMAGE_MIME_TYPES = MimeTypes()


def validate_content_type(image):
    return True


def image_upload(image: UploadFile):
    content_type = image.content_type
    file_extension = PurePath(image.filename).suffix
    validate_content_type(image)
    return image
