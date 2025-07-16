from pydantic import BaseModel
from typing import List, Optional

class ChartRequest(BaseModel):
    stk_cd: str  # 종목코드
    base_dt: str  # 기준일자 YYYYMMDD
    upd_stkpc_tp: str = "1"  # 수정주가구분 0 or 1

class ChartData(BaseModel):
    open_price: str
    current_price: str
    high_price: str
    low_price: str
    dt: str
    ma_5: Optional[float] = None
    ma_20: Optional[float] = None
    ma_60: Optional[float] = None
    ma_120: Optional[float] = None
    middle_band: Optional[float] = None
    upper_band: Optional[float] = None
    lower_band: Optional[float] = None

class ChartResponse(BaseModel):
    message: str
    data: List[ChartData]

class ErrorResponse(BaseModel):
    detail: str
