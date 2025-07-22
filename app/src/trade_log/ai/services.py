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
        "사용자가 입력한 매매일지를 분석하여, 다음 조건에 따라 평가와 피드백을 반드시 한글로 제공해 주세요.\n\n"
        "또한, 매매 당시 해당 종목의 재무제표, 실적 발표, 관련 뉴스, 그리고 시장 지수(KOSPI, 나스닥 등)나 업종 흐름을 검색하여 참고한 뒤, 가능한 경우 이를 분석에 반영해 주세요.\n\n"
        "감정 평가 시 영어로 된 감정을 제시해주는 한글로 대치해서 결과에 반영해 주세요. fear: 공포, impulse: 충동, anxiety: 불안, confidence: 확신, serenity: 무념무상\n\n"
        "---\n\n"
        "분석 항목 (총 100점 만점 기준 채점):\n\n"
        "1. **요약 평가**\n"
        "   - 전체 매매에 대한 평가를 3줄 이내로 요약\n\n"
        "2. **전략 평가**(45점)\n"
        "   - 기술적 진입/청산 판단은 적절했는가?\n"
        "   - 당시의 지수 흐름(KOSPI 등), 거래량, 업종 흐름은 전략에 어떤 영향을 미쳤는가?\n\n"
        "3. **기업 정보 기반 분석**(35점)\n"
        "   - 해당 시점의 실적, 뉴스, 재무 상태(PER, ROE, 부채비율 등)를 기반으로 이 종목의 매수는 합리적이었는가?\n\n"
        "4. **감정적 개입 여부**(20점)\n"
        "   - 조급한 매도, 손절 회피 등의 감정적 매매는 있었는가?\n\n"
        "5. **개선 제안**\n"
        "   - 시장과 종목 분석을 바탕으로 더 나은 전략이 있었는가?\n"
        "   - 다음 매매를 위한 조언을 3가지 이상 제공\n\n"
        "---\n\n"
        "출력 형식 요구:"
        "각 문항별 점수는 아래 기준에 따라 감점 및 가산을 적용하여 계산하세요.\n"
        "전략 평가 (45점): 진입/청산 이유 부실 시 -10, 시장 흐름 고려 없음 -5, 기술 지표 미사용 -5, 리스크 관리 없음 -5\n" 
        "기업 정보 평가 (35점): 실적·뉴스 언급 없음 -10, 재무지표 부재 -5, 업종 비교 없음 -3\n"  
        "감정 개입 (20점): 조급함 -5, 후회 표현 -3, 전략 대신 감정 주도 -5\n"
        "각 항목별 분석에 따라 이 기준을 바탕으로 정수 점수를 산출하세요.\n"
        "답변 시, 어떻게 점수를 계산했는지 알리지 말고 각 문항의 점수만 알려주세요.\n"
        "답변 시, 각 평가 요소를 'SEPARATOR'라는 단어로 나누고, 평가 요소와 평가 요소에 대한 답변 'SPLIT'이라는 단어로 나눠주세요. 각 영문자는 모두 대문자입니다.\n"
        "답변 시, 가장 상단에 아래 형식으로 각 항목별 점수를 1줄에 반환하세요.\n"  
        "45@35@20@"
        "답변 형식은 아래 형태를 참고하세요.\n"
        "45@35@20@1. **요약 평가**SPLIT1번 문항에 대한 답변SEPARATOR2. **전략평가**SPLIT2번 평가요소에 대한답변SEPARATOR3. ..."
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