from sqlalchemy.orm import Session
from sqlalchemy import text
from .schemas import StockRankSchema
from .model import TradeDetail

def get_stock_rank(db: Session):
    sql = """
        SELECT
            td.stock_name,
            td.stock_code,
            COUNT(*) AS order_count
        FROM trade_details td
        JOIN accounts acc ON td.account_id = acc.id
        JOIN users u ON acc.user_id = u.id
        GROUP BY td.stock_code, td.stock_name
        ORDER BY order_count DESC
        LIMIT 5;
    """
    result = db.execute(text(sql))
    # db.query(TradeDetail).add

    
    rows = result.fetchall()

    rank_list = [
        StockRankSchema(
            stock_name=row._mapping["stock_name"],
            stock_code=row._mapping["stock_code"],
            order_count=row._mapping["order_count"]
        )
        for row in rows
    ]
    return rank_list
