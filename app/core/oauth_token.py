from app.logging import log_error, log_info
from app.core.config import settings
from app.database.core import get_db
from app.src.account.repository import AccountRepository
import requests

async def get_oauth_token(user_id: str):
    """사용자별 OAuth 토큰 발급"""
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    try:
        # DB에서 사용자의 API 키 조회
        db = next(get_db())
        account_repo = AccountRepository(db)
        api_keys = account_repo.get_api_keys_by_user_id(user_id)
        
        if not api_keys:
            log_error(f'사용자의 API 키를 찾을 수 없음: user_id={user_id}')
            return None
        
        url = f'{settings.KIWOOM_BASE_URL}/oauth2/token'
        data = {
            'grant_type': 'client_credentials',
            'appkey': api_keys['app_key'],
            'secretkey': api_keys['secret_key'],
        }
        
 
        
        response = requests.post(url=url, headers=headers, json=data)
        
        log_info(f'OAuth 응답 상태 코드: {response.status_code}')
        log_info(f'OAuth 응답 텍스트: {response.text}')
        
        if response.status_code != 200:
            log_error(f'OAuth API 호출 실패: 상태코드 {response.status_code}, 응답: {response.text}')
            return None

        response_data = response.json()
        log_info(f'OAuth 응답 JSON: {response_data}')
        
        expires_dt = response_data.get('expires_dt')
        token_type = response_data.get('token_type')
        token = response_data.get('token')
        
        log_info(f'token_type: {token_type}, expires_dt: {expires_dt} token: {token}')

        if not token_type or not token:
            log_error(f'토큰 정보가 불완전함: token_type={token_type}, token={token}')
            return None

        return {"token": f'{token_type} {token}', "expires_dt": expires_dt}
    except Exception as e:
        log_error(f'oauth token 발급 오류 : {str(e)}')
        return None
    finally:
        if 'db' in locals():
            db.close()