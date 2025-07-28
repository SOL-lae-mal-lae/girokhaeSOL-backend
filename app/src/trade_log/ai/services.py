from app.logging import log_info
from .repository import AIRepository
from .schemas import AIAnalysisResponse, AILinkSchema
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
import requests

load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
BASE_URL = "https://api.perplexity.ai/chat/completions"

def get_perplexity_analysis(payload):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(BASE_URL,  json=payload, headers=headers)
        log_info(f"API 응답 상태 코드: {response.status_code}")
        
        if response.status_code != 200:
            log_info(f"API 호출 실패: {response.text}")
            return None, []
            
        data = response.json()
        log_info(f"API 응답 데이터: {data}")

        result_text = data["choices"][0]["message"]["content"]

        # 출처 링크 추출 (citations 활용)
        citations = data.get("citations", [])
        links = []
        if citations:
            for idx, url in enumerate(citations):
                if url:
                    links.append({
                        "news_link": url,
                        "sequence": idx + 1
                    })

        return result_text, links
        
    except Exception as e:
        log_info(f"API 호출 중 예외 발생: {str(e)}")
        return None, []


def analyze_trade_log(db: Session, trade_log_id: int) -> AIAnalysisResponse:
    repo = AIRepository(db)
    # 1. 기존 분석 결과 있으면 반환
    exist = repo.get_ai_analysis_by_log_id(trade_log_id)
    if exist:
        links = repo.get_ai_links_by_analysis_id(exist.id)
        return AIAnalysisResponse(
            id=exist.id,
            trade_log_id=exist.trade_log_id,
            result=exist.result,
            links=[AILinkSchema(news_link=l.news_link, sequence=l.sequence) for l in links] if links else None
        )

    # 2. DB에서 매매일지, 상세, 요약, 감정, 뉴스 등 조회
    trade_log = repo.get_trade_log_by_id(trade_log_id)
    trade_details = repo.get_trade_details_by_log_id(trade_log_id)
    trade_summary = repo.get_trade_summary_by_log_id(trade_log_id)
    sentiments = repo.get_sentiments_by_trade_log_id(trade_log_id)  # 감정 리스트
    news_links = repo.get_news_links_by_trade_log_id(trade_log_id)  # 뉴스 url 리스트
    if not trade_log:
        return None

    # 감정 문자열로 변환
    sentiment_str = ", ".join([s.name for s in sentiments]) if sentiments else ""
    # 뉴스 url 문자열로 변환
    news_str = "\n".join([n.url for n in news_links]) if news_links else ""

    # 3. 프롬프트 생성
    prompt = f"""
    <매매일지>
    - 날짜: {trade_log.date}
    - 투자 성향: {trade_log.investment_type}
    - 감정: {sentiment_str}
    - 종합 요약: {trade_summary}
    - 매매 상세 내역: {trade_details}
    - 매매 근거: {trade_log.rationale}
    - 매매 평가: {trade_log.evaluation}
    - 관련 뉴스: {news_str}
    """

    system_prompt = (
        "당신은 투자 전략 분석가 AI입니다.\n\n"
        "사용자가 입력한 매매일지를 냉철하고 현실적으로 분석하여, 다음 조건에 따라 평가와 피드백을 반드시 한글로 제공해 주세요. \n\n"
        "또한, 매매 당시 해당 종목의 재무제표, 실적 발표, 관련 뉴스, 그리고 시장 지수(KOSPI, 나스닥 등)나 업종 흐름을 검색하여 참고한 뒤, 가능한 경우 이를 분석에 반영해 주세요.\n\n"
        "감정 분석 시 아래 영어 감정 단어가 나오면 다음과 같이 한글로 번역하여 반영해 주세요:\n" 
        "- fear → 공포\n"
        "- impulse → 충동\n"
        "- anxiety → 불안\n"
        "- confidence → 확신\n"
        "- serenity → 무념무상\n\n"       
        "---\n\n"
        "분석 항목 (총 100점 만점 기준 채점)\n\n"
        "1. **피드백 요약**\n"
        "   - 전체 매매에 대한 피드백을 3줄 이내로 요약\n\n"
        "2. **전략 분석**(50점)\n"
        "   - 기술적 진입/청산 판단은 적절했는가?\n"
        "   - 당시의 지수 흐름(KOSPI 등), 거래량, 업종 흐름은 전략에 어떤 영향을 미쳤는가?\n\n"
        "3. **기업 정보 기반 분석**(50점)\n"
        "   - 해당 시점의 실적, 뉴스, 재무 상태(PER, ROE, 부채비율 등)를 기반으로 이 종목의 매수는 합리적이었는가?\n\n"
        "4. **개선 제안**\n"
        "   - 시장과 종목 분석을 바탕으로 더 나은 전략이 있었는가?\n"
        "   - 다음 매매를 위한 조언을 3가지 이상 제공\n\n"
        "5. **점수 채점\n"
        "   - 전략 분석 점수와 기업 정보 기반 분석 점수 계산 이유를 제공\n\n"
        "---\n\n"
        "출력 형식 지침 (엄격히 따르세요)\n\n"
        "1. 가장 상단에 아래 형식으로 각 항목별 점수를 1줄에 반환하세요.(공백 없이, 정수만)\n"  
        "전략 분석 점수@기업 정보 기반 분석 점수@\n"
        "2. 각 항목은 다음 구조로 나눠 작성하세요(각 영문자는 모두 대문자):\n"
        "- 항목 제목과 본문 구분: SPLIT\n"
        "- 본문 내 문장 간 구분: PARAGRAPH\n"
        "- 항목 간 구분: SEPARATOR\n"
        "- 본문의 마지막 문장 끝에는 PARAGRAPH를 쓰지 마세요.\n\n"
        "예시:\n"
        "32@40@1. **피드백 요약**SPLIT1번 문항에 대한 답변 문장1PARAGRAPH문장2PARAGRAPH문장3SEPARATOR2. **전략 분석**SPLIT2번 문항에 대한답변 문장1PARAGRAPH문장2PARAGRAPH문장3SEPARATOR3. ..."
    )

    # 4. GPT 호출
    payload = {
        "model":"sonar-pro",
        "messages" :[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens":2500,
    }
    result_text, links = get_perplexity_analysis(payload)

    # 5. DB 저장
    ai_analysis_id = repo.save_ai_analysis(trade_log_id, result_text)

    # 출처 링크 저장
    if links:
        repo.save_ai_links(ai_analysis_id, links)

    # DB에서 다시 읽어오기
    db_links = repo.get_ai_links_by_analysis_id(ai_analysis_id)

    # 7. 응답
    return AIAnalysisResponse(
        id=ai_analysis_id,
        trade_log_id=trade_log_id,
        result=result_text,
        links=[AILinkSchema(news_link=l.news_link, sequence=l.sequence) for l in db_links] if db_links else None
    )

def get_trade_log_by_date(db :Session, user_id: str,date: str):
    repo = AIRepository(db)
    result = repo.get_trade_log_by_date(user_id, date)

    return result.id if result else None