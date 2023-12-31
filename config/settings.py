"""
FOREX TRADING CONFIGURATION
"""
# Line Developer
CHANNEL_ID = '2000419904'
CHANNEL_SECRET = 'de235b7898ef01c99c2e2719e96ac8f7'
CHANNEL_ACCESS = 'PbuTedhOuBM/xM/AUT9sgF9ReK5wubQt54zdEjR7sZY60kMIlDTkD8tfMFV2Ejp0ooXe14tMt/uLPiCeD1Ex2IrDMwLlDwXgdL1m' \
                 'xKSH3ke++3y9wbbCmhaxsDZ5EhfVM+hCuXg6hpJ5Crgks0lNzAdB04t89/1O/w1cDnyilFU='

ADMIN_ID = 'U336a0fca075c76dec4776367b1c93ce4'

TOKEN = 'YWRtaW46NTQ2ZHEhJzxkQl0iVUc3KEJC'

USE_TZ = True
TIME_ZONE = 'Asia/Bangkok'

# Line developer max corousel contents
MAXIMUM_ITEMS = 12

# Constant

# This is set to 70. The RSI value of 70 is commonly used as a threshold to determine if a currency pair is overbought.
# When the RSI goes above this value, it might be a signal for traders to consider selling.
OVERBOUGHT = 70
# This is set to 30. RSI value of 30 or below is typically seen as an indication that a currency pair may be oversold.
# This might be interpreted by traders as a buying opportunity.
OVERSOLD = 30

ALERT_VALUE_INDICATOR = 4

INTERVAL = ['M1', 'M5', 'M15', 'M30', 'H1', 'H2', 'H4', 'D1']

PREFIX = 'FX_IDC:'

ICON_UP = 'https://cdn.pic.in.th/file/picinth/up-arrow.png'
ICON_DOWN = 'https://cdn.pic.in.th/file/picinth/up-arrow-1.png'

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

# A mapping of timeframes to their respective index ranges in the indicator list
INDICATOR_INTERVAL_RANGE = {
    'M1': (16, 22),
    'M5': (22, 28),
    'M15': (28, 34),
    'M30': (34, 40),
    'H1': (40, 46),
    'H2': (46, 52),
    'H4': (52, 58),
    'D1': (58, 64)
}

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
