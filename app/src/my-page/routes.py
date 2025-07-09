from fastapi import APIRouter, HTTPException
from app.src.test.repository import insert_test, get_tests

router = APIRouter(prefix="/test", tags=["test"])

@router.get("/db-connection")
async def test_db_connection():
    """데이터베이스 연결 테스트"""
    try:
        # 간단한 테스트 데이터 삽입
        insert_test("connection_test")
        
        # 테스트 데이터 조회
        results = get_tests()
        
        return {
            "status": "success",
            "message": "데이터베이스 연결 성공!",
            "data": {
                "inserted": True,
                "total_records": len(results),
                "sample_data": results[-5:] if results else []  # 최근 5개 레코드
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"데이터베이스 연결 실패: {str(e)}"
        )

@router.post("/insert")
async def insert_test_data(name: str):
    """테스트 데이터 삽입"""
    try:
        insert_test(name)
        return {
            "status": "success",
            "message": f"'{name}' 데이터가 성공적으로 삽입되었습니다."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"데이터 삽입 실패: {str(e)}"
        )

@router.get("/list")
async def list_test_data():
    """테스트 데이터 조회"""
    try:
        results = get_tests()
        return {
            "status": "success",
            "message": "테스트 데이터 조회 성공",
            "data": {
                "total_count": len(results),
                "records": results
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"데이터 조회 실패: {str(e)}"
        )
