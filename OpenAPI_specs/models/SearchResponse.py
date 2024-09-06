from pydantic import BaseModel, Field
from .SearchMatch import SearchMatch
from typing import List
from typing import Optional


class SearchResponse(BaseModel):
    query: Optional[str] = Field(None, alias='query')
    from_field: Optional[int] = Field(None, alias='from')
    page: Optional[int] = Field(None, alias='page')
    pageSize: Optional[int] = Field(None, alias='pageSize')
    provider: Optional[str] = Field(None, alias='provider')
    total: Optional[int] = Field(None, alias='total')
    matches: Optional[List[SearchMatch]] = Field(None, alias='matches')
    maxScore: Optional[float] = Field(None, alias='maxScore')

    class Config:
        from_attributes = True
