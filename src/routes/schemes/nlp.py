from pydantic import BaseModel
from typing import Optional

class IndexPushRequest(BaseModel):
    
    do_reset: Optional[int] = 0

class SearchIndexRequest(BaseModel):
    
    text: str
    limit: Optional[int] = 5