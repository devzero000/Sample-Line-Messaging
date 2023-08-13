import json

import requests

import config.api as api
import config.settings as settings
from utils import timezone


def get_currency_pair_description(currency: str) -> tuple:
    """
    Generate currency pair name and its description.

    Parameters:
        currency (str): Currency symbol string from data entry (e.g., "EURUSD").

    Returns:
        tuple: A tuple containing the currency name and its description.
    """

    name = currency.replace(settings.PREFIX, '')
    base_currency, quote_currency = name[:3], name[3:]
    description = f'{settings.CURRENCY[base_currency]} vs {settings.CURRENCY[quote_currency]}'

    return name, description, base_currency, quote_currency


def get_signal(indicator: list) -> str:
    indicator = indicator[8:16]

    positive_count = sum(1 for num in indicator if num > 0)
    negative_count = sum(1 for num in indicator if num < 0)

    if positive_count > negative_count:
        return 'UP TREND'
    elif negative_count > positive_count:
        return 'DOWN TREND'
    else:
        return 'NEURAL'


def get_status(indicator: list) -> list:
    """
    Analyzes the provided indicator values and returns a list of states where
    the value is either overbought or oversold based on defined settings.

    Args:
    - indicator (list): List of indicator values.

    Returns:
    - list: A list of dictionaries containing 'value' and 'timeframe'.
    """

    states = []
    indicator = indicator[:8]

    # Iterate over the indicator values and their corresponding intervals simultaneously.
    for value, interval in zip(indicator, settings.INTERVAL):

        # Check if the value is either overbought or oversold.
        if value >= settings.OVERBOUGHT or value <= settings.OVERSOLD:
            states.append({
                'value': '%.2f' % value,
                'timeframe': interval
            })

    return states


def tract_fibo(indicator: list, tf: str) -> dict:
    scope = None

    if tf not in settings.INTERVAL:
        return {}

    if tf == 'M1':
        scope = indicator[16:22]
    elif tf == 'M5':
        scope = indicator[22:28]
    elif tf == 'M15':
        scope = indicator[28:34]
    elif tf == 'M30':
        scope = indicator[34:40]
    elif tf == 'H1':
        scope = indicator[40:46]
    elif tf == 'H2':
        scope = indicator[46:52]
    elif tf == 'H4':
        scope = indicator[52:58]
    elif tf == 'D1':
        scope = indicator[58:64]

    fib = {
        'R3': str('%.5f' % scope[0]),
        'R2': str('%.5f' % scope[1]),
        'R1': str('%.5f' % scope[2]),
        'S1': str('%.5f' % scope[3]),
        'S2': str('%.5f' % scope[4]),
        'S3': str('%.5f' % scope[5])
    }
    return fib


def extract_forex_info(data: dict) -> dict:
    """
    Extract Forex information from given data.

    Parameters:
        data (dict): Raw data containing Forex information.

    Returns:
        dict: A dictionary containing extracted Forex information or an error message.
    """

    forex_entries = data.get('data', [])

    if not forex_entries:
        return {'error': 'Data not found!'}

    forex_info = {}
    for entry in forex_entries:
        currency = entry.get('s')
        indicator = entry.get('d')

        if currency:
            name, desc, base_currency, quote_currency = get_currency_pair_description(currency)
            status = get_status(indicator)

            if status:
                for info in status:
                    timeframe = info["timeframe"]
                    key = f'{name}_{timeframe}'
                    load_fibo = tract_fibo(indicator, timeframe)
                    forex_info[key] = {
                        'symbol': name,
                        'base_currency': base_currency,
                        'quote_currency': quote_currency,
                        'value': info['value'],
                        'timeframe': info['timeframe'],
                        'signal': get_signal(indicator),
                        'description': desc,
                    }
                    forex_info[key] = {**forex_info[key], **load_fibo}

    return forex_info


def post_data_to_tradingview(url: str, header: dict, payload: json):
    """
    Post the provided payload to the TradingView API and return the response data.
    """
    response = requests.post(url, headers=header, data=payload)

    # Check for any errors in the API call
    response.raise_for_status()

    return response.json()


def generate_bubble_string(info: dict) -> dict:
    symbol = info['symbol']
    desc = info['desc']
    trend = info['signal']
    timeframe = info['timeframe']
    value = info['value']
    is_up_trend = bool(trend == 'UP TREND')

    detail = timezone.localtime().strftime("%Y.%m.%d %H.%M")

    bubble_string = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": trend,
                    "weight": "bold",
                    "color": "#1DB446" if is_up_trend else "#f5314b",
                    "size": "sm"
                },
                {
                    "type": "text",
                    "text": symbol,
                    "weight": "bold",
                    "size": "xxl",
                    "margin": "md"
                },
                {
                    "type": "text",
                    "text": desc,
                    "size": "xs",
                    "color": "#aaaaaa",
                    "wrap": True
                },
                {
                    "type": "text",
                    "text": f"Timeframe: {timeframe} - {value}%",
                    "color": "#000000",
                    "align": "start",
                    "size": "xs",
                    "gravity": "center",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "filler"
                                }
                            ],
                            "width": f"{value}%",
                            "backgroundColor": "#2edb02" if is_up_trend else "#ff2424",
                            "height": "6px"
                        }
                    ],
                    "backgroundColor": "#f0f0f2",
                    "height": "6px",
                    "margin": "sm"
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "xxl",
                    "spacing": "sm",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "weight": "bold",
                                    "text": "Pivots",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "weight": "bold",
                                    "text": "Fibonacci",
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "separator",
                            "color": "#FFFFFF",
                            "margin": "sm"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Resistance #3",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": info['R3'],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Resistance #2",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": info['R2'],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Resistance #1",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": info['R1'],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Support #1",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": info['S1'],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Support #2",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": info['S2'],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Support #3",
                                    "size": "sm",
                                    "color": "#555555",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": info['S3'],
                                    "size": "sm",
                                    "color": "#111111",
                                    "align": "end"
                                }
                            ]
                        },
                    ]
                },
                {
                    "type": "separator",
                    "margin": "xxl"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "TIMESTAMP",
                            "size": "xs",
                            "color": "#aaaaaa",
                            "flex": 0
                        },
                        {
                            "type": "text",
                            "text": f"#{detail}",
                            "color": "#aaaaaa",
                            "size": "xs",
                            "align": "end"
                        }
                    ]
                }
            ]
        },
        "styles": {
            "footer": {
                "separator": True
            }
        }
    }
    return bubble_string


def generate_corousel_content():
    info = get_info()

    corousel_string = {
        "type": "carousel",
        "contents": [
            get_payload_for_bubble(instance, generate_bubble_string) for _, instance in info.items()
        ]
    }
    return json.dumps(corousel_string)


def get_payload_for_bubble(instance, func):
    payload = {
        'symbol': instance['symbol'],
        'desc': instance['description'],
        'signal': instance['signal'],
        'value': instance['value'],
        'timeframe': instance['timeframe'],
        'R3': instance['R3'],
        'R2': instance['R2'],
        'R1': instance['R1'],
        'S1': instance['S1'],
        'S2': instance['S2'],
        'S3': instance['S3'],
    }
    return func(payload)


def get_info():
    payload = settings.BASE_PAYLOAD
    json_payload = json.dumps(payload, indent=4)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {settings.TOKEN}'
    }
    res = post_data_to_tradingview(url=api.TRADINGVIEW, header=headers, payload=json_payload)

    data = extract_forex_info(res)
    return data
