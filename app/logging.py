import logging
from logging.handlers import RotatingFileHandler
import os

try:
    print("✅ Services import 성공!")
except ImportError as e:
    print(f"❌ Services import 실패: {e}")

# logs 디렉토리가 존재하지 않으면 생성
if not os.path.exists("logs"):
    os.makedirs("logs")

# 로그 파일 경로 정의
log_file = "logs/app.log"

# 로거 생성
logger = logging.getLogger(__name__)

# 로깅 레벨 설정
logger.setLevel(logging.DEBUG)

# 타임스탬프, 로그 레벨, 실제 메시지를 추가하는 포매터 정의
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 콘솔 핸들러 (터미널 출력)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 파일 핸들러 (UTF-8)
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1_000_000,
    backupCount=3,
    encoding="utf-8"               # ✅ 인코딩 추가
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 에러 로그 전용 핸들러 (UTF-8)
error_log_file = "logs/error.log"
error_file_handler = RotatingFileHandler(
    error_log_file,
    maxBytes=1_000_000,
    backupCount=3,
    encoding="utf-8"               # ✅ 인코딩 추가
)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(formatter)
logger.addHandler(error_file_handler)

# 검증 샘플 로그
logger.debug("로깅 설정 완료. (UTF-8 인코딩 확인)")

# 샘플 유틸리티 함수들
def log_debug(message: str):
    logger.debug(message)

def log_info(message: str):
    logger.info(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str):
    logger.error(message)

def log_critical(message: str):
    logger.critical(message)
