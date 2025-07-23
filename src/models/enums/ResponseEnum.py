from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size too large"
    FILE_UPLOADED_SUCCESS = "File is uploaded successfully"
    FILE_UPLOADED_FAILED = "File upload failed"
