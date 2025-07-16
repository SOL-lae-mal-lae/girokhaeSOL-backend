import requests
from typing import List
from .schemas import ChartData, ChartRequest
import pandas as pd
import numpy as np

class ChartService:
    def __init__(self):
        self.host = 'https://mockapi.kiwoom.com'
        self.token = None
        self.token_type = None
        self.expires_dt = None

    def _get_chart_data(self, request: ChartRequest) -> dict:
        """주식일봉차트조회요청"""

        endpoint = '/api/dostk/chart'
        url = self.host + endpoint

        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': self.token,
            'cont-yn': 'N', #계속 데이터를 받을지 설정
            'next-key': '',
            'api-id': 'ka10081',
        }

        data = {
            'stk_cd': request.stk_cd,
            'base_dt': request.base_dt,
            'upd_stkpc_tp': request.upd_stkpc_tp,
        }

        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"차트 데이터 조회 실패: {response.text}")

    def _transform_chart_data(self, raw_data: dict) -> List[ChartData]:
        chart_data_list = []
        if 'stk_dt_pole_chart_qry' in raw_data:
            df = pd.DataFrame(raw_data['stk_dt_pole_chart_qry'])
            df = df.rename(columns={
                'open_pric': 'open',
                'cur_prc': 'close',
                'high_pric': 'high',
                'low_pric': 'low',
                'dt': 'dt'
            })
            for col in ['open', 'close', 'high', 'low']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df.sort_values('dt')
            df['ma_5'] = df['close'].rolling(window=5).mean()
            df['ma_20'] = df['close'].rolling(window=20).mean()
            df['ma_60'] = df['close'].rolling(window=60).mean()
            df['ma_120'] = df['close'].rolling(window=120).mean()
            # 볼린저밴드 계산 (20일 기준, 표준편차 2)
            df['middle_band'] = df['ma_20']
            df['stddev'] = df['close'].rolling(window=20).std()
            df['upper_band'] = df['middle_band'] + (2 * df['stddev'])
            df['lower_band'] = df['middle_band'] - (2 * df['stddev'])
            for idx in df.index:
                row = df.loc[idx]
                chart_data = ChartData(
                    open_price=str(row['open']) if not np.isnan(row['open']) else "0",
                    current_price=str(row['close']) if not np.isnan(row['close']) else "0",
                    high_price=str(row['high']) if not np.isnan(row['high']) else "0",
                    low_price=str(row['low']) if not np.isnan(row['low']) else "0",
                    dt=str(row['dt']),
                    ma_5=float(row['ma_5']) if not np.isnan(row['ma_5']) else None,
                    ma_20=float(row['ma_20']) if not np.isnan(row['ma_20']) else None,
                    ma_60=float(row['ma_60']) if not np.isnan(row['ma_60']) else None,
                    ma_120=float(row['ma_120']) if not np.isnan(row['ma_120']) else None,
                    middle_band=float(row['middle_band']) if not np.isnan(row['middle_band']) else None,
                    upper_band=float(row['upper_band']) if not np.isnan(row['upper_band']) else None,
                    lower_band=float(row['lower_band']) if not np.isnan(row['lower_band']) else None,
                )
                chart_data_list.append(chart_data)
        else:
            chart_data = ChartData(
                open_price="0",
                current_price="0",
                high_price="0",
                low_price="0",
                dt="20000101"
            )
            chart_data_list.append(chart_data)
        return chart_data_list

    def get_chart_data(self, request: ChartRequest, token: str) -> List[ChartData]:
        try:
            self.token = token
            raw_data = self._get_chart_data(request)
            return self._transform_chart_data(raw_data)
        except Exception as e:
            raise Exception(f"차트 데이터 처리 중 오류 발생: {str(e)}")
