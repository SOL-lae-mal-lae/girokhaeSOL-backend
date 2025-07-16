from sqlalchemy.orm import Session
from typing import Any
from fastapi import HTTPException
from app.logging import log_debug, log_info, log_error
from app.src.trade_log.month_trade_log.model import TradeDetail, Sentiment
from app.src.trade_log.month_trade_log.schemas import TradeLogTransactionResponse
from .repository import TradeLogRepository
import requests

from app.core.config import settings


class TradeLogService:
    repository: TradeLogRepository

    def __init__(self, db: Session = None):
        if db:
            self.repository = TradeLogRepository(db)

    def get_monthly_trade_logs_by_user_id(self, user_id: str, year_month: str) -> dict[
        str, list[Any] | TradeDetail | list[Sentiment] | Any]:
        try:

            log_info(f"Service 시작: user_id = {user_id}, year_month = {year_month}")

            # Repository 호출
            log_debug("Repository 호출 시작")
            trade_logs = self.repository.get_monthly_trade_logs_by_user_id(user_id, year_month)
            log_debug(f"Repository 결과: {len(trade_logs)}개의 레코드")

            log_debug("Repository 호출 시작")
            trade_details = self.repository.get_monthly_trade_stat_by_user_id(user_id, year_month)
            log_debug(f"Repository 결과: {len(trade_details)}개의 레코드")

            # 가장 많이 선택한 감정 유형
            log_debug("Repository 호출 시작")
            sentiment_counts = self.repository.get_monthly_trade_log_sentiments_by_user_id(user_id, year_month)
            log_debug(f"Repository 결과: {len(sentiment_counts)}개의 레코드")

            # 가장 많이 선택된 감정 추출 (동률이 있으면 여러 개)
            sentiments = []
            if sentiment_counts:
                max_count = sentiment_counts[0].count
                # 최대 카운트와 같은 감정들만 필터링
                for sentiment_count in sentiment_counts:
                    if sentiment_count.count == max_count:
                        sentiments.append(sentiment_count.name)
                    else:
                        break  # 내림차순 정렬되어 있으므로 더 작은 카운트가 나오면 중단

            # 가장 많이 투자한 종목
            log_debug("Repository 호출 시작")
            top_invested_stocks = self.repository.get_monthly_top_invested_stocks_by_user_id(user_id, year_month)
            log_debug(f"Repository 결과: {len(top_invested_stocks)}개의 레코드")

            # 날짜 추출
            dates = []
            top_buy = []

            for trade_log in trade_logs:
                if trade_log.date:
                    dates.append(trade_log.date.strftime('%Y-%m-%d'))

            # 가장 많이 투자한 종목을 문자열 리스트로 변환
            for stock in top_invested_stocks:
                top_buy.append(stock.stock_name)

            log_info(f"최종 결과: {len(dates)}개의 날짜")

            return {
                "dates": dates,
                "total_buy_amount": trade_details['total_buy_amount'],
                "total_sell_amount": trade_details['total_sell_amount'],
                "profit_rate": trade_details['profit_rate'],
                "total_commission_and_tax": trade_details['total_commission_and_tax'],
                "top_buy": top_buy,
                "sentiment": sentiments,
            }
        except Exception as e:
            log_error(f"get_monthly_trade_logs_by_user_id 실패: {str(e)}")
            log_error(f"Exception 타입: {type(e)}")
            import traceback
            log_error(f"Traceback: {traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=f"오류가 발생했습니다: {str(e)}")

    def get_transaction_from_kiwoom(self, date: str, token: str, cont_yn: str = 'N',
                                    next_key: str = ''):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': token,
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': 'ka10170'
        }
        data = {
            "base_dt": "".join(date.split('-')),
            "ottks_tp": "2",
            "ch_crd_tp": "0"
        }
        try:
            response = requests.post(url=f'{settings.KIWOOM_BASE_URL}/api/dostk/acnt', headers=headers, json=data)
            res = response.json()

            # 빈 문자열을 적절한 기본값으로 변환하는 헬퍼 함수
            def safe_float(value, default=0.0):
                if value == '' or value is None:
                    return default
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default
            
            def safe_int(value, default=0):
                if value == '' or value is None:
                    return default
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return default
            
            trade_details = []
            
            # tdy_trde_diary가 존재하고 비어있지 않을 때만 처리
            if 'tdy_trde_diary' in res and res['tdy_trde_diary'] and len(res['tdy_trde_diary']) > 0:
                log_debug(f"거래 내역 처리 시작: {len(res['tdy_trde_diary'])}개 항목")
                for item in res['tdy_trde_diary']:
                    # 모든 값이 '0'이거나 빈 값인지 확인하는 함수
                    def is_empty_trade(item):
                        # 주식명이나 주식코드가 있으면 실제 거래로 간주
                        if item.get('stk_nm') and item.get('stk_nm') != '0' and item.get('stk_nm') != '':
                            return False
                        if item.get('stk_cd') and item.get('stk_cd') != '0' and item.get('stk_cd') != '':
                            return False
                        return True
                    
                    # 빈 거래 내역이면 건너뛰기
                    if is_empty_trade(item):
                        continue
                    
                    trade_details.append({
                        "stock_name": item.get('stk_nm', ''),
                        "stock_code": item.get('stk_cd', ''),
                        "avg_buy_price": safe_float(item.get('buy_avg_pric')),
                        "buy_quantity": safe_int(item.get('buy_qty')),
                        "avg_sell_price": safe_float(item.get('sel_avg_pric')),
                        "sell_quantity": safe_int(item.get('sell_qty')),
                        "cmsn_alm_tax": safe_float(item.get('cmsn_alm_tax')),
                        "profit_amount": safe_int(item.get('pl_amt')),
                        "profit_rate": safe_float(item.get('prft_rt'))
                    })
            else:
                log_debug("거래 내역이 없어서 빈 배열 반환")

            data = {
                "summaries": {
                    "total_buy_amount": safe_int(res.get('tot_buy_amt')),
                    "total_sell_amount": safe_int(res.get('tot_sell_amt')),
                    "total_cmsn_tax": safe_float(res.get("tot_cmsn_tax")),
                    "settlement_amount": safe_int(res.get('tot_pl_amt')),
                    "profit_rate": safe_float(res.get('tot_prft_rt'))
                },
                "trade_details": trade_details
            }

            return data
        except Exception as e:
            raise HTTPException(status_code=500, detail=f'kiwoom api ka10170 호출에서 오류가 발생했습니다.{e}')
