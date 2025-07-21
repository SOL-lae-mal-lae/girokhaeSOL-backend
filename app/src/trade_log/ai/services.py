from .repository import AIRepository
from .schemas import AIAnalysisResponse, AILinkSchema
from openai import OpenAI
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session

load_dotenv()

API_KEY = os.getenv("PERPLEXITY_API_KEY", "")
BASE_URL = "https://api.perplexity.ai"

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
        "사용자가 입력한 매매일지를 분석하여, 다음 조건에 따라 평가와 피드백을 한글로 제공해 주세요.\n\n"
        "또한, 매매 당시 해당 종목의 재무제표, 실적 발표, 관련 뉴스, 그리고 시장 지수(KOSPI, 나스닥 등)나 업종 흐름을 검색하여 참고한 뒤, 가능한 경우 이를 분석에 반영해 주세요.\n\n"
        "---\n\n"
        "분석 항목 (총 100점 만점 기준 채점):\n\n"
        "1. **요약 평가**\n"
        "   - 전체 매매에 대한 평가를 3줄 이내로 요약\n"
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
        "1. 가장 상단에 아래 형식으로 각 항목별 점수를 정수로 1줄에 반환하세요 (기계가 파싱할 수 있게 구체적인 형식으로):"  
        "40@30@18@" 
    )

    # 4. GPT 호출
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2500,
    )
    result_text = response.choices[0].message.content

    # 출처 링크 추출 (citations 활용)
    citations = getattr(response, "citations", None)
    links = []
    if citations:
        for idx, url in enumerate(citations):
            if url:
                links.append({
                    "news_link": url,
                    "sequence": idx + 1
                })

    # 5. DB 저장
    ai_analysis_id = repo.save_ai_analysis(trade_log_id, result_text)

    # 출처 링크 저장
    if links:
        repo.save_ai_links(ai_analysis_id, links)

    # 7. 응답
    return AIAnalysisResponse(
        id=ai_analysis_id,
        trade_log_id=trade_log_id,
        result=result_text,
        links=[AILinkSchema(**link) for link in links] if links else None
    )
