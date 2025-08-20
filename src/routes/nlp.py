from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from .schemes import IndexPushRequest, SearchIndexRequest
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
        

@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(request: Request, project_id: str):
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vector_db_client=request.app.vector_db_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )

    collection_info = nlp_controller.get_vector_db_collection_info(project=project)


    return JSONResponse(
        content={
            "signal": ResponseSignal.GET_INDEX_INFO_SUCCESS.value,
            "collection_info": collection_info
        }
    )


@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request, project_id: str, search_request: SearchIndexRequest):

    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    nlp_controller = NLPController(
        vector_db_client=request.app.vector_db_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )

    results = nlp_controller.search_vector_db_collection(
        project=project,
        query=search_request.text,
        limit=search_request.limit
    )

    if not results:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.SEARCH_INDEX_FAILED.value
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.SEARCH_INDEX_SUCCESS.value,
            "results": [result.dict() for result in results]
        }
    )
    

    