from sqlalchemy.orm import Session
from .model import TradeLog, TradeSummary, TradeDetail, Chart, NewsLink, TradeLogAccount, Sentiment, TradeLogSentiment

class TradeLogDetailRepository:
    def __init__(self, db: Session):
        self.db = db

    def insert_trade_log(self, user_id, body):
        trade_log = TradeLog(
            user_id=user_id,
            date=body.date,
            investment_type=body.investment_type,
            rationale=body.rationale,
            evaluation=body.evaluation
        )
        self.db.add(trade_log)
        self.db.flush()
        return trade_log.id

    def insert_trade_summary(self, trade_log_id, summary):
        trade_summary = TradeSummary(
            trade_log_id=trade_log_id,
            total_buy_amount=summary.total_buy_amount,
            total_sell_amount=summary.total_sell_amount,
            settlement_amount=summary.settlement_amount,
            profit_rate=summary.profit_rate,
            total_cmsn_tax=summary.total_cmsn_tax
        )
        self.db.add(trade_summary)

    def insert_trade_details(self, trade_log_id, details):
        is_inserted = False
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
            self.db.add(trade_detail)
            if not is_inserted:
                self.db.merge(TradeLogAccount(trade_log_id=trade_log_id, account_id=d.account_id))
                is_inserted = True
    def insert_charts(self, trade_log_id, charts):
        for c in charts:
            chart = Chart(
                trade_log_id=trade_log_id,
                stock_code=c.stock_code,
                start_date=c.start_date,
                end_date=c.end_date,
                sequence=c.sequence
            )
            self.db.add(chart)

    def insert_news_links(self, trade_log_id, news_links):
        for n in news_links:
            news = NewsLink(
                trade_log_id=trade_log_id,
                url=n.url
            )
            self.db.add(news)

    def insert_sentiments(self, trade_log_id, sentiments):
        for s in sentiments:
            sentiment = self.db.query(Sentiment).filter_by(name=s).first()
            if sentiment:
                self.db.add(TradeLogSentiment(trade_log_id=trade_log_id, sentiment_id=sentiment.id))
