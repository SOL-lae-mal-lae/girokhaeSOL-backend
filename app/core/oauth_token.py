from app.logging import log_error, log_info
from app.core.config import settings
import requests

async def get_oauth_token():
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    try:
        response = requests.post(url=f'{settings.KIWOOM_API_URL}/oauth2/token', headers=headers, data={
        'grant_type': 'client_credentials',
        'appkey': settings.KIWOOM_APP_KEY,
        'secretkey': settings.KIWOOM_SECRET_KEY,
        })

        expires_dt, token_type, token = response.json()
        log_info(f'token_type: {token_type}, expires_dt: {expires_dt} token: {token}')

        return {"token": f'{token_type} {token}', "expires_dt": expires_dt}
    except Exception as e:
        log_error(f'oauth token 발급 오류 : {str(e)}')