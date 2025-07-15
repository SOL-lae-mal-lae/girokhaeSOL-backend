from fastapi import APIRouter, HTTPException, status, Request
from .schemas import ChartRequest, ChartResponse, ErrorResponse
from .service import ChartService

router = APIRouter()

@router.post(
    "/chart",
    response_model=ChartResponse,
    responses={
        200: {"model": ChartResponse, "description": "차트 데이터 조회 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."},
        500: {"model": ErrorResponse, "description": "서버 내부 오류가 발생했습니다."}
    }
)
def get_chart_data(request: Request, chart_request: ChartRequest):
    """
    주식 차트 데이터를 조회합니다.
    
    - **stk_cd**: 종목코드 (예: 005930)
    - **base_dt**: 기준일자 (YYYYMMDD 형식, 예: 20241108)
    - **upd_stkpc_tp**: 수정주가구분 (0 또는 1, 기본값: 1)
    """
    try:
        token = request.state.token
        service = ChartService()
        chart_data = service.get_chart_data(chart_request, token)
        return {"message": "차트 불러오기 완료", "data": chart_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"차트 데이터 조회 중 오류가 발생했습니다: {str(e)}"
        )
