from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database.core import SessionLocal
from .schemas import PostCreateRequest, PostUpdateRequest, PostCreateResponse, PostDetailResponse, PostListResponseWrapper, PostDeleteResponse, ErrorResponse
from .services import PostService
from app.database.core import get_db

router = APIRouter()

@router.get(
    "",
    response_model=PostListResponseWrapper,
    responses={
        200: {"model": PostListResponseWrapper, "description": "게시글 조회 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def get_all_posts(
    db: Session = Depends(get_db)
):
    try:
        service = PostService(db)
        result = service.get_all_posts()
        return {"message": "게시글 조회 완료", "data": result}
    except Exception as e:
        print(f"Error getting all posts: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.get(
    "/general",
    response_model=PostListResponseWrapper,
    responses={
        200: {"model": PostListResponseWrapper, "description": "일반글 조회 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def get_general_posts(
    db: Session = Depends(get_db)
):
    try:
        service = PostService(db)
        result = service.get_general_posts()
        return {"message": "일반글 조회 완료", "data": result}
    except Exception as e:
        print(f"Error getting general posts: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.get(
    "/trade-log",
    response_model=PostListResponseWrapper,
    responses={
        200: {"model": PostListResponseWrapper, "description": "매매일지글 조회 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def get_trade_log_posts(
    db: Session = Depends(get_db)
):
    try:
        service = PostService(db)
        result = service.get_trade_log_posts()
        return {"message": "매매일지글 조회 완료", "data": result}
    except Exception as e:
        print(f"Error getting trade_log posts: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.post(
    "",
    response_model=PostCreateResponse,
    responses={
        201: {"model": PostCreateResponse, "description": "게시글 생성 완료"},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def create_post(
    body: PostCreateRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    try:
        service = PostService(db)
        user_id = request.state.user

        result = service.create_post(body, user_id)
       
    except Exception as e:
        print(f"Error creating post: {str(e)}")
        raise HTTPException(status_code=400, detail=f"포스트 생성 시, 오류가 발생했습니다: {str(e)}")

    try:
        final_result = service.create_tags_with_post_id(result['id'], body.tags)
        # final_result가 dict임을 보장하므로 그대로 반환
        return {"message": "success", "data": final_result}
    except Exception as e:
        print(f"Error creating post: {str(e)}")
        raise HTTPException(status_code=400, detail=f"태그 리스트 생성 시, 오류가 발생했습니다: {str(e)}")

@router.get(
    "/{post_id}",
    response_model=PostDetailResponse,
    responses={
        200: {"model": PostDetailResponse, "description": "게시글 조회 완료"},
        404: {"model": ErrorResponse, "description": "게시글을 찾을 수 없습니다."},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    try:
        service = PostService(db)
        result = service.get_post_by_id(post_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        
        return {"message": "success", "data": {"result": result}}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting post: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.put(
    "/{post_id}",
    response_model=PostDetailResponse,
    responses={
        200: {"model": PostDetailResponse, "description": "게시글 수정 완료"},
        404: {"model": ErrorResponse, "description": "게시글을 찾을 수 없습니다."},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def update_post(
    post_id: int,
    request: PostUpdateRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    try:
        # 사용자 ID 가져오기
        user_id = getattr(http_request.state, "user", None)
        # if not user_id:
        #     raise HTTPException(status_code=401, detail="인증이 필요합니다.")

        # trade_log_id가 0이면 None으로 처리
        if request.trade_log_id == 0:
            request.trade_log_id = None

        service = PostService(db)
        
        # 게시글 작성자 확인
        if not service.check_post_ownership(post_id, user_id):
            raise HTTPException(status_code=403, detail="게시글을 수정할 권한이 없습니다.")
        
        result = service.update_post(post_id, request)
        
        if not result:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        
        return {"message": "success", "data": result}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating post: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

@router.delete(
    "/{post_id}",
    response_model=PostDeleteResponse,
    responses={
        200: {"model": PostDeleteResponse, "description": "게시글 삭제 완료"},
        404: {"model": ErrorResponse, "description": "게시글을 찾을 수 없습니다."},
        400: {"model": ErrorResponse, "description": "오류가 발생했습니다."}
    }
)
def delete_post(
    post_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # 사용자 ID 가져오기
        user_id = getattr(request.state, "user", None)
        # if not user_id:
        #     raise HTTPException(status_code=401, detail="인증이 필요합니다.")

        service = PostService(db)
        
        # 게시글 작성자 확인
        if not service.check_post_ownership(post_id, user_id):
            raise HTTPException(status_code=403, detail="게시글을 삭제할 권한이 없습니다.")
        
        success = service.delete_post(post_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        
        return {"message": "success"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting post: {str(e)}")
        raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")
