from app.logging import log_error, log_info
from app.core.config import settings
from app.database.core import get_db
from app.src.account.repository import AccountRepository
import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Hash import MD5



def evpkdf(password, salt, key_size=32, iv_size=16):
    """
    CryptoJS의 EvpKDF 방식 구현 (MD5, 1회 반복)
    """
    d = b''
    while len(d) < key_size + iv_size:
        data = (d[-16:] if d else b'') + password + salt
        d += MD5.new(data).digest()
    return d[:key_size], d[key_size:key_size+iv_size]

def decrypt_data(encrypted_data: str) -> str:
    """CryptoJS AES 복호화 (EvpKDF 방식)"""
    try:
        encrypted_data_bytes = base64.b64decode(encrypted_data)
        assert encrypted_data_bytes[:8] == b'Salted__'
        salt = encrypted_data_bytes[8:16]
        ciphertext = encrypted_data_bytes[16:]
        key = settings.ENCRYPTION_KEY.encode()
        aes_key, aes_iv = evpkdf(key, salt)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=aes_iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        decrypted = unpad(decrypted_padded, AES.block_size)
        return decrypted.decode('utf-8')
    except Exception as e:
        log_error(f"복호화 중 오류 발생: {e}")
        raise e

async def get_oauth_token(user_id: str):
    """사용자별 OAuth 토큰 발급"""
    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }
    try:
        log_info(f"🔍 OAuth 토큰 발급 시작 - user_id: {user_id}")

        db = next(get_db())
        account_repo = AccountRepository(db)

        # 대표 계좌 기준으로 API 키 조회
        api_keys = account_repo.get_api_keys_of_primary_account(user_id)

        log_info(f"🔍 DB에서 조회한 API 키: {api_keys}")

        if not api_keys:
            log_error(f'사용자의 대표 계좌 API 키를 찾을 수 없음: user_id={user_id}')
            return None

        # 복호화된 키 사용
        print(f"[DEBUG] app_key 복호화 시도")
        decrypted_app_key = decrypt_data(api_keys['app_key'])
        print(f"[DEBUG] secret_key 복호화 시도")
        decrypted_secret_key = decrypt_data(api_keys['secret_key'])

        log_info(f"🔍 복호화된 키:")
        log_info(f"  - app_key: {decrypted_app_key}")
        log_info(f"  - secret_key: {decrypted_secret_key}")
     



        url = f'{settings.KIWOOM_BASE_URL}/oauth2/token'
        data = {
            'grant_type': 'client_credentials',
            'appkey': decrypted_app_key,
            'secretkey': decrypted_secret_key,
        }

    
        log_info(f"🔍 요청 데이터: {data}")
     
        response = requests.post(url=url, headers=headers, json=data)

        log_info(f'OAuth 응답 상태 코드: {response.status_code}')
      
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

async def register_account(user_id: str, app_key: str, secret_key: str):
    """계좌 등록 및 토큰 발급 후 DB 저장"""
    try:
        log_info(f"🔍 계좌 등록 시작 - user_id: {user_id}")

        db = next(get_db())
        account_repo = AccountRepository(db)

        # 계좌 정보 저장
        account_repo.save_account(user_id, app_key, secret_key)
        log_info(f"🔍 계좌 정보 저장 완료 - user_id: {user_id}")

        # 토큰 발급
        token_data = await get_oauth_token(user_id)

        if not token_data:
            log_error(f"🔍 토큰 발급 실패 - user_id: {user_id}")
            return None

        # 발급된 토큰 DB 저장
        account_repo.update_token(user_id, token_data['token'], token_data['expires_dt'])
        log_info(f"🔍 토큰 저장 완료 - user_id: {user_id}")

        return token_data
    except Exception as e:
        log_error(f"계좌 등록 중 오류 발생: {e}")
        return None
    finally:
        if 'db' in locals():
            db.close()