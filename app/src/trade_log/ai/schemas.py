from pydantic import BaseModel
from typing import List, Optional

class AILinkSchema(BaseModel):
    news_link: str
    sequence: int

class AIAnalysisResponse(BaseModel):
    id: int
    trade_log_id: int
    result: str
    links: Optional[List[AILinkSchema]] = None
