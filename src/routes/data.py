from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Setting
from controllers import DataController, ProjectController, PorcessController
from models import ResponseSignal
from .schemes import ProcessRequest
import os
import aiofiles
import logging


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Setting = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid , signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
             content={
                "signal": signal
                }
        )

    project_dir_path = ProjectController().get_project_dir(project_id=project_id)
    file_name = data_controller.generate_unique_file_name(org_file_name=file.filename, project_id=project_id)

    file_path = os.path.join(project_dir_path , file_name)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        
        logger.error(f"File upload failed: {e}")

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseSignal.FILE_UPLOADED_FAILED.value
                }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file name": file_name
            }
    )
    

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str , process_request: ProcessRequest):

    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = PorcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunck_size=chunk_size,
        overlap_size=overlap_size
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
                }
        )    
    return file_chunks