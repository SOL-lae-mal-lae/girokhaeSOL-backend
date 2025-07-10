---
## ✅ 개발환경 세팅
---

### 가상환경 설치

> 가상환경 설치로 깨끗한 환경에서 시작해주세요  
> (혹시 pip 패키지들 충돌 방지하기 위함)

```
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
```

---

### 라이브러리 설치

requirements.txt 를 기준으로 설치:

```
pip install -r requirements.txt
```

---

### .env

루트 디렉토리에 추가

---

### uvicorn 실행 (FastAPI 예시)

```
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- `app.main` → main.py 위치 기준 (모듈 경로)
- `app` → FastAPI 인스턴스 변수명
- `--reload` → 코드 변경 시 서버 자동 재시작

---

---

참고) 추후 디렉토리 생성 시 모든 폴더에  
`__init__.py` 넣어줘야함. **설사! 빈 파일이라도 상관없어요.**  
파이썬이 해당 디렉토리를 패키지로 인식해서 추후 import하기 위함임.

---

참고2) model import 시  
같은 디렉토리 안에 있으면

```
from .model import TradeDetail  # .model.py 가 같은 디렉토리에 있으면 이런 식으로 표기
```

아니라면..

```
from app.database.model import Base
```

이런 식으로 **모든 경로를 작성해주어야 하며**,  
파이썬은 슬래시가 아닌 `.` 온점으로 경로를 구분함 참고.

---

참고3) 파이썬 변수명으로  
하이픈 못써요. `"-"` 못씀. 언더바 `"_"` 써야 해요.

---

## 🗂️ 디렉토리 설명

---

## ⚙️ 설계 컨셉

### 도메인 분리 개발

- 하나의 앱 안에서 모든 기능을 뒤섞지 않고,
- **도메인 단위로 폴더를 분리**
- 각 도메인은 독립적으로 개발 및 유지보수 가능

---

### `app/core`

미들웨어/db config (데이터베이스 host, 비번 등 관리)

- **공통 설정이나 유틸리티 모듈**을 두는 곳

---

### `database`

- DB 연결 및 ORM 설정
  - DB 엔진 생성
  - Base 클래스 선언 (SQLAlchemy Base 등)

---

### `src` 실제 우리가 개발 제일 많이할 곳

도메인으로 디렉토리 분리  
ex) `http://127.0.0.1:8000/api/v1/data_lab`

> 이 엔드포인트에 필요한  
> 함수 / 루트 정의

- 실제 **서비스 도메인 코드가 들어가는 최상위 폴더**
- 각 도메인별로 폴더로 분리되어 있음 (도메인 분리 설계)

  - `account` → 회원, 계좌 관련 도메인
  - `auth` → 인증/인가 모듈
  - `community` → 커뮤니티 기능
  - `data_lab` → 데이터 분석, 집계
  - `my-page` → 마이페이지, 유저 개인 정보 관리

- 각 도메인 폴더 안에는 **MVC 구조**로 파일이 배치됨
  - **Model** → DB 모델 정의
  - **route.py** → 라우터, 컨트롤러 (API 엔드포인트)
  - **Service** → 비즈니스 로직 처리
  - **schemas** → API 처리
    **repository** -> db연결

---

### `main.py`

> 진입점. 여기에 router 선언

---

### `logging.py`

디버깅 코드 / 에러 코드 터미널에서 볼 수 있도록 도와주는 모듈입니다.  
(오류 추적하기 편리해요)

---

## ✅ 개발 시 참고 (엔드포인트 prefix)

우리 엔드포인트

```
localhost:8000/api/v1
```

으로 고정했어요.  
ex) `http://127.0.0.1:8000/api/v1/test-db`

그래서 router 추가 시 prefix 항상 넣어줘야 함.

---

### Router 추가 시 prefix 예제

```
app.include_router(rank_router, prefix="/api/v1")

```

---
