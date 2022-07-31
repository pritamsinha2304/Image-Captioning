""" Holds the schema for file validation """

# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument

from fastapi import File, UploadFile
from pydantic import BaseModel, validator


class FormData(BaseModel):
    """Form Data

    Args:
        BaseModel (_type_): Base Model

    Returns:
        FormData
    """
    imagefileinput: UploadFile

    @validator('imagefileinput')
    def validate_file(cls, data):
        """Validate File

        Args:
            data (_type_): _description_
        """
        def __validate_extension(data):
            if not data.filename.endswith(('.jpg', '.jpeg', '.png')):
                return False
            return True

        def __validate_signature(data):
            sig = data.content_type
            if sig not in ['image/jpeg', 'image/png']:
                return False
            return True

        extension = __validate_extension(data)
        signature = __validate_signature(data)

        if extension and signature:
            return data
        if not extension and signature:
            return ValueError("Invalid File Format")
        if not signature and extension:
            return ValueError("Invalid File Signature")
        return ValueError("Invalid File Format and Signature")

    @classmethod
    def as_form(cls, imagefileinput: UploadFile = File(...)):
        """Return Form Data

        Args:
            file (UploadFile): Uploaded file. Defaults to File(...).

        Returns:
            FormData
        """
        return cls(imagefileinput=imagefileinput)
