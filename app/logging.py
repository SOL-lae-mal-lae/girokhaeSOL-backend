import logging
from logging.handlers import RotatingFileHandler
import os

# 모든 services 함수들 import
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
logger.setLevel(logging.DEBUG)  # 모든 레벨 캡처: DEBUG, INFO, WARNING, ERROR, CRITICAL

# 타임스탬프, 로그 레벨, 실제 메시지를 추가하는 포매터 정의
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 터미널에 로그를 출력하는 콘솔 핸들러
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 파일에 로그를 기록하는 파일 핸들러, 1MB 후 로그 로테이션
file_handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=3)  # 1 MB, 백업 파일 3개
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 선택사항: 에러 로그를 위한 두 번째 파일
error_log_file = "logs/error.log"
error_file_handler = RotatingFileHandler(error_log_file, maxBytes=1e6, backupCount=3)
error_file_handler.setLevel(logging.ERROR)  # 이 파일에는 ERROR와 CRITICAL만 기록
error_file_handler.setFormatter(formatter)
logger.addHandler(error_file_handler)

# 검증을 위한 샘플 로그 메시지
logger.debug("로깅 설정 완료.")

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
