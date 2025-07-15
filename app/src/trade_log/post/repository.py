from sqlalchemy.orm import Session
from .model import TradeSummary, Chart, NewsLink, TradeLogAccount
from app.src.trade_log.model import TradeLog, TradeDetail, TradeLogSentiment, Sentiment

def insert_trade_log(db: Session, user_id, body):
    trade_log = TradeLog(
        user_id=user_id,
        date=body.date,
        investment_type=body.investment_type,
        rationale=body.rationale,
        evaluation=body.evaluation
    )
    db.add(trade_log)
    db.flush()  # id 생성
    return trade_log.id

def insert_trade_summary(db: Session, trade_log_id, summary):
    trade_summary = TradeSummary(
        trade_log_id=trade_log_id,
        total_buy_amount=summary.total_buy_amount,
        total_sell_amount=summary.total_sell_amount,
        settlement_amount=summary.settlement_amount,
        profit_rate=summary.profit_rate,
        total_cmsn_tax=summary.total_cmsn_tax
    )
    db.add(trade_summary)

def insert_trade_details(db: Session, trade_log_id, details):
    for d in details:
        trade_detail = TradeDetail(
            trade_log_id=trade_log_id,
            account_id=d.account_id,
            stock_name=d.stock_name,
            stock_code=d.stock_code,
            avg_buy_price=d.avg_buy_price,
            buy_quantity=d.buy_quantity,
            avg_sell_price=d.avg_sell_price,
            sell_quantity=d.sell_quantity,
            cmsn_alm_tax=d.cmsn_alm_tax,
            profit_amount=d.profit_amount,
            profit_rate=d.profit_rate
        )
        db.add(trade_detail)
        # trade_log_accounts도 함께 추가
        db.merge(TradeLogAccount(trade_log_id=trade_log_id, account_id=d.account_id))

def insert_charts(db: Session, trade_log_id, charts):
    for c in charts:
        chart = Chart(
            trade_log_id=trade_log_id,
            stock_code=c.stock_code,
            start_date=c.start_date,
            end_date=c.end_date,
            sequence=c.sequence
        )
        db.add(chart)

def insert_news_links(db: Session, trade_log_id, news_links):
    for n in news_links:
        news = NewsLink(
            trade_log_id=trade_log_id,
            url=n.url
        )
        db.add(news)

def insert_sentiments(db: Session, trade_log_id, sentiments):
    for s in sentiments:
        sentiment = db.query(Sentiment).filter_by(name=s).first()
        if sentiment:
            db.add(TradeLogSentiment(trade_log_id=trade_log_id, sentiment_id=sentiment.id))
