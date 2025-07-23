from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.core import get_db
from .schemas import CommentCreateRequest, CommentUpdateRequest, CommentCreateResponse, CommentListResponseWrapper, CommentDeleteResponse, CommentUpdateResponse, ErrorResponse
from .services import CommentService

router = APIRouter()

@router.post(
    "/{post_id}/comments",
    response_model=CommentCreateResponse,
    responses={
        201: {"model": CommentCreateResponse, "description": "댓글 생성 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def create_comment(
    post_id: int,
    request: CommentCreateRequest,
    db: Session = Depends(get_db)
):
    try:
        #user_id = "user_2zceSsp2uVsMkLuh8AftIRulD4F"  # 임시 사용자 ID
        user_id = getattr(request.state, "user", None)

        service = CommentService(db)
        result = service.create_comment(request, post_id, user_id)
        return {"message": "success", "data": result}
    except Exception as e:
        print(f"Error creating comment: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.get(
    "/{post_id}/comments",
    response_model=CommentListResponseWrapper,
    responses={
        200: {"model": CommentListResponseWrapper, "description": "댓글 조회 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = CommentService(db)
        result = service.get_comments_by_post_id(post_id)
        return {"message": "댓글 조회 완료", "data": result}
    except Exception as e:
        print(f"Error getting comments: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.delete(
    "/{post_id}/comments/{comment_id}",
    response_model=CommentDeleteResponse,
    responses={
        200: {"model": CommentDeleteResponse, "description": "댓글 삭제 완료"},
        404: {"model": ErrorResponse, "description": "댓글을 찾을 수 없습니다."},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def delete_comment(
    post_id: int,
    comment_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # 사용자 ID 가져오기
        #user_id = "user_2zceSsp2uVsMkLuh8AftIRulD4F"
        user_id = getattr(request.state, "user", None)
        # if not user_id:
        #     raise HTTPException(status_code=401, detail="인증이 필요합니다.")

        service = CommentService(db)
        
        # 댓글 작성자 확인
        if not service.check_comment_ownership(comment_id, user_id):
            raise HTTPException(status_code=403, detail="댓글을 삭제할 권한이 없습니다.")
        
        success = service.delete_comment(comment_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
        
        return {"message": "success"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting comment: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.put(
    "/{post_id}/comments/{comment_id}",
    response_model=CommentUpdateResponse,
    responses={
        200: {"model": CommentUpdateResponse, "description": "댓글 수정 완료"},
        404: {"model": ErrorResponse, "description": "댓글을 찾을 수 없습니다."},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def update_comment(
    post_id: int,
    comment_id: int,
    request: CommentUpdateRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    try:
        # 사용자 ID 가져오기
        #user_id = "user_2zceSsp2uVsMkLuh8AftIRulD4F"
        user_id = getattr(http_request.state, "user", None)
        # if not user_id:
        #     raise HTTPException(status_code=401, detail="인증이 필요합니다.")

        service = CommentService(db)
        
        # 댓글 작성자 확인
        if not service.check_comment_ownership(comment_id, user_id):
            raise HTTPException(status_code=403, detail="댓글을 수정할 권한이 없습니다.")
        
        result = service.update_comment(comment_id, request)
        
        if not result:
            raise HTTPException(status_code=404, detail="댓글을 찾을 수 없습니다.")
        
        return {"message": "success", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating comment: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")
