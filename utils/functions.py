import functools
import json

import requests
from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    ReplyMessageRequest,
    FlexMessage,
    FlexContainer, TextMessage,
)

import config.api as api
import config.settings as settings
import flex.template as template


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


def generate_corousel_content():
    info = get_info()

    # Breaking down the info into chunks of 12
    chunks = [dict(list(info.items())[i:i + settings.MAXIMUM_ITEMS])
              for i in range(0, len(info), settings.MAXIMUM_ITEMS)]

    all_carousels = []
    for chunk in chunks:
        corousel_string = {
            "type": "carousel",
            "contents": [
                get_payload_for_bubble(
                    instance,
                    template.generate_bubble_string)
                for _, instance in chunk.items()
            ]
        }
        all_carousels.append(json.dumps(corousel_string))

    return all_carousels


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


def get_info(is_task=False):
    payload = settings.BASE_PAYLOAD
    json_payload = json.dumps(payload, indent=4)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {settings.TOKEN}'
    }
    res = post_data_to_tradingview(url=api.TRADINGVIEW, header=headers, payload=json_payload)

    if is_task:
        return res

    data = extract_forex_info(res)
    return data


def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split('.'))


def push_message(event=None, content=None, **kwargs):
    from main import configuration  # fix circular import

    is_task = kwargs.get('is_task', False)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        """
        # If you want the system to handle messages that users type in, by detecting 
        # from the event message (received message), you can explore Dialogflow for further implementation.
        receive_text = event.message.text
        """

        if not content and not is_task:
            return line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=getattr(event, 'reply_token', event),
                    messages=[TextMessage(text='No interesting currency pairs found.')]
                )
            )

        if len(content) > settings.MAXIMUM_ITEMS and not is_task:
            message = FlexMessage(alt_text="Overtrade Signal", contents=FlexContainer.from_json(content[0]))
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=getattr(event, 'reply_token', event),
                    messages=[message],
                    timeout=60
                )
            )
        else:
            for items in content:
                message = FlexMessage(alt_text="Overtrade Signal", contents=FlexContainer.from_json(items))
                line_bot_api.push_message(
                    PushMessageRequest(
                        to=rgetattr(event, 'source.user_id', event),
                        messages=[message],
                        timeout=60
                    )
                )
