from app.logging import log_error, log_info
from app.core.config import settings
import requests

async def get_oauth_token():
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    try:
        url = f'{settings.KIWOOM_BASE_URL}/oauth2/token'
        data = {
            'grant_type': 'client_credentials',
            'appkey': settings.KIWOOM_APP_KEY,
            'secretkey': settings.KIWOOM_SECRET_KEY,
        }
        
        log_info(f'OAuth 요청 URL: {url}')
        log_info(f'OAuth 요청 데이터: {data}')
        log_info(f'OAuth 요청 헤더: {headers}')
        
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