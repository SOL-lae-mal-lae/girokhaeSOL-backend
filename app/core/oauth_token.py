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
        log_info(f"🔍 OAuth 토큰 발급 시작 - user_id: {user_id}")
        
        db = next(get_db())
        account_repo = AccountRepository(db)

        api_keys = account_repo.get_api_keys_by_user_id(user_id)
        
        log_info(f"🔍 DB에서 조회한 API 키: {api_keys}")
        
        if not api_keys:
            log_error(f'사용자의 API 키를 찾을 수 없음: user_id={user_id}')
            return None
        
        log_info(f"🔍 키움 API 호출 준비:")
        log_info(f"  - app_key: {api_keys['app_key']}")
        log_info(f"  - secret_key: {api_keys['secret_key'][:10]}...")  # 보안상 일부만 출력
        
        url = f'{settings.KIWOOM_BASE_URL}/oauth2/token'
        data = {
            'grant_type': 'client_credentials',
            'appkey': api_keys['app_key'],
            'secretkey': api_keys['secret_key'],
        }
        
        log_info(f"🔍 요청 URL: {url}")
        log_info(f"🔍 요청 데이터: {data}")
        
 
        
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