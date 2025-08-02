from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Setting
from controllers import DataController, ProjectController, PorcessController
from models import ResponseSignal
from .schemes import ProcessRequest
import os
import aiofiles
import logging
from models import ProjectModel, ChunkModel, AssetModel, AssetTypeEnum
from models.db_schemes import DataChunk, Asset
from bson import ObjectId


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)


@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, 
                        file: UploadFile,  app_settings: Setting = Depends(get_settings)):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )


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

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    asset_resources = Asset(
        asset_project_id= project.id,
        asset_name= file_name,
        asset_type= AssetTypeEnum.FILE.value,
        asset_size= os.path.getsize(file_path)
    )
    asset_record = await asset_model.create_asset(asset=asset_resources)
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file name": str(asset_record.id)
            }
    )
    

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str , process_request: ProcessRequest):

    # file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    asset_model = await AssetModel.create_instance(
        db_client=request.app.db_client
    )

    project_files_ids = {}
    if process_request.file_id:
        asset_record = await asset_model.get_asset_record(
            asset_project_id=project.id,
            asset_name=process_request.file_id
        )
        
        if asset_record is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.FILE_NOT_FOUND.value
                    }
            )
        project_files_ids = {
            asset_record.id: asset_record.asset_name
        }
    else:

        project_files = await asset_model.get_all_project_assets(
            asset_project_id=project.id,
            asset_type=AssetTypeEnum.FILE.value
        )

        project_files_ids = {
            record.id: record.asset_name
            for record in project_files
        }

    if len(project_files_ids) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.NO_FILES_FOUND.value
                }
        )

    process_controller = PorcessController(project_id=project_id)

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    no_records = 0
    no_files = 0

    if do_reset:
        
        await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    for asset_id , file_id in project_files_ids.items():
        file_content = process_controller.get_file_content(file_id=file_id)

        if file_content is None:
            logger.error(f"File content is None for file id: {file_id}")
            continue

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
        
        file_chunks_records = [
            DataChunk(
                chunk_text=chunk.page_content,
                chunk_metadata=chunk.metadata,
                chunk_order=i+1,
                chunk_project_id=project.id,
                chunk_asset_id=asset_id
            )
            for i, chunk in enumerate(file_chunks)
        ]


        no_records += await chunk_model.insert_many_chunks(file_chunks_records)
        no_files += 1

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_PROCESSED_SUCCESS.value,
            "inserted_chunks": no_records,
            "processed_files": no_files
        }
    )

    
