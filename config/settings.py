"""
FOREX TRADING CONFIGURATION
"""
# Line Developer
CHANNEL_ID = '2000392888'
CHANNEL_SECRET = '25646cc5f5615b25ce8eda12b3f183c6'
CHANNEL_ACCESS = 'U6AH6Pe1BY+YJWuKwlCN7b2AbNzYvJ0z6DXqR0DAjqCj9GA0CfKRfa3vHThCRjG9Z/13RHaKZiKUUYPWWjeVzPmVIDgKD14NDfk34' \
                 'grvZ30fkdPPvpSissFWUAfcVKft0WpGu0RQxtgDbE0ONUF6kQdB04t89/1O/w1cDnyilFU='

TOKEN = 'YWRtaW46NTQ2ZHEhJzxkQl0iVUc3KEJC'

USE_TZ = True
TIME_ZONE = 'Asia/Bangkok'

# Constant

# This is set to 70. The RSI value of 70 is commonly used as a threshold to determine if a currency pair is overbought.
# When the RSI goes above this value, it might be a signal for traders to consider selling.
OVERBOUGHT = 70
# This is set to 30. RSI value of 30 or below is typically seen as an indication that a currency pair may be oversold.
# This might be interpreted by traders as a buying opportunity.
OVERSOLD = 30

INTERVAL = ['M1', 'M5', 'M15', 'M30', 'H1', 'H2', 'H4', 'D1']

PREFIX = 'FX_IDC:'

CURRENCY = {
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'EUR': 'Euro',
    'CHF': 'Swiss Franc',
    'GBP': 'Great Britain Poud',
    'JPY': 'Japanese Yen',
    'NZD': 'New Zealand Dollar',
    'USD': 'US Dollar',
}

# The following are combinations of currencies for which we analyze trading data:
FOREX_GROUP = [
    'AUDCAD',
    'AUDCHF',
    'AUDJPY',
    'AUDUSD',
    'CADCHF',
    'CADJPY',
    'CHFJPY',
    'EURAUD',
    'EURCAD',
    'EURCHF',
    'EURGBP',
    'EURJPY',
    'EURUSD',
    'GBPAUD',
    'GBPCAD',
    'GBPJPY',
    'GBPUSD',
    'NZDCAD',
    'NZDCHF',
    'NZDJPY',
    'NZDUSD',
    'USDCAD',
    'USDCHF',
    'USDJPY',
]

BASE_PAYLOAD = {
    'symbols': {
        'tickers': [f'{PREFIX}{currency}' for currency in FOREX_GROUP],
        'query': {
            'types': [
                'forex'
            ]
        }
    },
    'columns': [
        'RSI|1',
        'RSI|5',
        'RSI|15',
        'RSI|30',
        'RSI|60',
        'RSI|120',
        'RSI|240',
        'RSI',

        'MACD.macd|1',
        'MACD.macd|5',
        'MACD.macd|15',
        'MACD.macd|30',
        'MACD.macd|60',
        'MACD.macd|120',
        'MACD.macd|240',
        'MACD.macd',

        "Pivot.M.Fibonacci.R3|1",
        "Pivot.M.Fibonacci.R2|1",
        "Pivot.M.Fibonacci.R1|1",
        "Pivot.M.Fibonacci.S1|1",
        "Pivot.M.Fibonacci.S2|1",
        "Pivot.M.Fibonacci.S3|1",

        "Pivot.M.Fibonacci.R3|5",
        "Pivot.M.Fibonacci.R2|5",
        "Pivot.M.Fibonacci.R1|5",
        "Pivot.M.Fibonacci.S1|5",
        "Pivot.M.Fibonacci.S2|5",
        "Pivot.M.Fibonacci.S3|5",

        "Pivot.M.Fibonacci.R3|15",
        "Pivot.M.Fibonacci.R2|15",
        "Pivot.M.Fibonacci.R1|15",
        "Pivot.M.Fibonacci.S1|15",
        "Pivot.M.Fibonacci.S2|15",
        "Pivot.M.Fibonacci.S3|15",

        "Pivot.M.Fibonacci.R3|30",
        "Pivot.M.Fibonacci.R2|30",
        "Pivot.M.Fibonacci.R1|30",
        "Pivot.M.Fibonacci.S1|30",
        "Pivot.M.Fibonacci.S2|30",
        "Pivot.M.Fibonacci.S3|30",

        "Pivot.M.Fibonacci.R3|60",
        "Pivot.M.Fibonacci.R2|60",
        "Pivot.M.Fibonacci.R1|60",
        "Pivot.M.Fibonacci.S1|60",
        "Pivot.M.Fibonacci.S2|60",
        "Pivot.M.Fibonacci.S3|60",

        "Pivot.M.Fibonacci.R3|120",
        "Pivot.M.Fibonacci.R2|120",
        "Pivot.M.Fibonacci.R1|120",
        "Pivot.M.Fibonacci.S1|120",
        "Pivot.M.Fibonacci.S2|120",
        "Pivot.M.Fibonacci.S3|120",

        "Pivot.M.Fibonacci.R3|240",
        "Pivot.M.Fibonacci.R2|240",
        "Pivot.M.Fibonacci.R1|240",
        "Pivot.M.Fibonacci.S1|240",
        "Pivot.M.Fibonacci.S2|240",
        "Pivot.M.Fibonacci.S3|240",

        "Pivot.M.Fibonacci.R3",
        "Pivot.M.Fibonacci.R2",
        "Pivot.M.Fibonacci.R1",
        "Pivot.M.Fibonacci.S1",
        "Pivot.M.Fibonacci.S2",
        "Pivot.M.Fibonacci.S3",
    ]
}
