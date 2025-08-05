from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from .schemes import IndexPushRequest
from models import ProjectModel, ChunkModel
from models.enums.ResponseEnum import ResponseSignal
from controllers import NLPController
import logging

logger = logging.getLogger('uvicorn.error')


nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"]
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request, project_id: str, push_request: IndexPushRequest):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "signal": ResponseSignal.PROJECT_NOT_FOUND_ERROR.value
            }
        )
    
    nlp_controller = NLPController(
        vector_db_client=request.app.vector_db_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )

    has_records = True
    page_no = 1
    inserted_chunk_count = 0
    idx  = 0

    while has_records:
        page_chunks = await chunk_model.get_poject_chunks(project_id=project.id, page_no=page_no)
        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            continue
        
        page_no += 1

        chunk_ids = list(range(idx, idx + len(page_chunks)))
        idx += len(page_chunks)

        is_inserted = nlp_controller.index_into_vector_db(
            project=project,
            chunks=page_chunks,
            chunks_ids=chunk_ids,
            do_reset=push_request.do_reset
        )

        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignal.INSERT_INTO_VECTOR_DB_FAILED.value
                }
            )
        
        inserted_chunk_count += len(page_chunks)
    
    return JSONResponse(
        content={
            "signal": ResponseSignal.INSERT_INTO_VECTOR_DB_SUCCESS.value,
            "inserted_chunks": inserted_chunk_count
        }
    )
        

    
    

    