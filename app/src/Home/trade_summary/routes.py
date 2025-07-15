from fastapi import APIRouter, HTTPException, status, Request
from .schemas import HomeSummaryResponse, HomeSummaryData, ErrorResponse
from .services import HomeService
from app.logging import log_info, log_error

router = APIRouter()

@router.get(
    "/summary",
    response_model=HomeSummaryResponse,
    summary="사용자 홈 요약 정보 조회",
    description="키움 API를 통해 사용자의 계좌 요약 정보를 조회합니다",
    responses={
        200: {"description": "계좌 요약 정보 조회 완료"},
        400: {"model": ErrorResponse, "description": "잘못된 요청입니다"},
        404: {"model": ErrorResponse, "description": "사용자를 찾을 수 없습니다"},
        422: {"model": ErrorResponse, "description": "유효성 검증에 실패했습니다"},
        500: {"model": ErrorResponse, "description": "서버 내부 오류"}
    }
)
async def get_user_summary(
    start_date: str = "20250705", 
    end_date: str = "20250715",
    request: Request = None
):
    """사용자 홈 요약 정보를 조회합니다"""
    
    try:
        token = getattr(request.state, 'token', None) if request else None
        
        # 쿼리 파라미터를 딕셔너리로 구성
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        log_info(f"사용자 홈 요약 정보 조회 요청: params={params}")
        
        service = HomeService()
        result = service.get_user_summary(token=token, params=params)

        
        if "error" in result:
            log_error(f"사용자 홈 요약 정보 조회 실패: {result['error']}")
            
            # 에러 타입에 따른 HTTP 상태 코드 설정
            if "찾을 수 없음" in result["error"]:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="사용자를 찾을 수 없습니다."
                )
            elif "유효성" in result["error"]:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="유효성 검증에 실패했습니다."
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="잘못된 요청입니다."
                )
        
        # 성공 응답 구조 생성 - HomeSummaryResponse 모델에 맞게
        # HomeSummaryResponse 모델 인스턴스 생성
        summary_data = result["data"]
        data_obj = HomeSummaryData(
           
            id=summary_data["id"],
            journal_count_year=summary_data["journal_count_year"],
            cumulative_investment_principal=summary_data["cumulative_investment_principal"],
            cumulative_profit_loss=summary_data["cumulative_profit_loss"],
            cumulative_profit_rate=summary_data["cumulative_profit_rate"]
        )
        
        response = HomeSummaryResponse(
            message="계좌 요약 정보 조회 완료",
            data=data_obj
        )
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"사용자 홈 요약 정보 조회 중 예외 발생: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="서버 내부 오류가 발생했습니다"
        )

