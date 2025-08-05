from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File type not supported"
    FILE_SIZE_EXCEEDED = "File size too large"
    FILE_UPLOADED_SUCCESS = "File is uploaded successfully"
    FILE_UPLOADED_FAILED = "File upload failed"
    FILE_PROCESSING_FAILED = "File processing failed"
    FILE_PROCESSED_SUCCESS = "File processed successfully"
    NO_FILES_FOUND = "No files found"
    FILE_NOT_FOUND= "File not found"
    PROJECT_NOT_FOUND_ERROR= "Project not found"
    INSERT_INTO_VECTOR_DB_FAILED = "Insert into vector db failed"
    INSERT_INTO_VECTOR_DB_SUCCESS = "Insert into vector db success"
    GET_INDEX_INFO_SUCCESS = "Get index info success"
    SEARCH_INDEX_SUCCESS = "Search index success"
    SEARCH_INDEX_FAILED = "Search index failed"
    
    
