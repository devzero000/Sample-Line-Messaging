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
    """
    Determine the trend of financial data based on positive or negative indicators.

    Parameters:
    - indicator (list): A list of numerical indicators where positive values represent positive signals
                        and negative values represent negative signals. The function specifically
                        focuses on the indicators in the index range [8:16].

    Returns:
    - str: 'UPTREND' if there are more positive indicators,
           'DOWNTREND' if there are more negative indicators,
           'NEUTRAL' if the number of positive and negative indicators are equal.
    """

    # Filter relevant indicators.
    relevant_indicators = indicator[8:16]

    # Count positive and negative indicators.
    positive_count = sum(1 for num in relevant_indicators if num > 0)
    negative_count = sum(1 for num in relevant_indicators if num < 0)

    # Determine trend.
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


def extract_fibo(indicator: list, tf: str) -> dict:
    """
    Extracts Fibonacci values based on the given timeframe (tf).

    Parameters:
    - indicator (list): List containing the indicator values.
    - tf (str): Timeframe, e.g., 'M1', 'M5', etc.

    Returns:
    - dict: A dictionary containing the Fibonacci values.
            If the given timeframe is not valid, an empty dictionary is returned.
    """

    # A mapping of timeframes to their respective index ranges in the indicator list
    INTERVAL_RANGE = settings.INDICATOR_INTERVAL_RANGE

    if tf not in INTERVAL_RANGE:
        return {}

    start, end = INTERVAL_RANGE[tf]
    scope = indicator[start:end]

    fib = {
        'R3': f'{scope[0]:.5f}',
        'R2': f'{scope[1]:.5f}',
        'R1': f'{scope[2]:.5f}',
        'S1': f'{scope[3]:.5f}',
        'S2': f'{scope[4]:.5f}',
        'S3': f'{scope[5]:.5f}'
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

        if not currency:
            continue

        name, desc, base_currency, quote_currency = get_currency_pair_description(currency)
        status = get_status(indicator)

        if not status:
            continue

        for info in status:
            timeframe = info["timeframe"]
            key = f'{name}_{timeframe}'
            forex_info[key] = {
                'symbol': name,
                'base_currency': base_currency,
                'quote_currency': quote_currency,
                'value': info['value'],
                'timeframe': info['timeframe'],
                'signal': get_signal(indicator),
                'description': desc,
                **extract_fibo(indicator, timeframe)
            }

    return forex_info


def post_data_to_tradingview(url: str, header: dict, payload: json):
    """
    Post the provided payload to the TradingView API and return the response data.
    """
    response = requests.post(url, headers=header, data=payload)

    # Check for any errors in the API call
    response.raise_for_status()

    return response.json()


def generate_carousel_content():
    """
    Generates carousel content based on the information fetched.

    This function retrieves information and then breaks it down
    into chunks of maximum allowed items (as defined in settings).
    Each chunk of information is then processed to get a carousel string
    and appended to a list of all carousels.

    Returns:
        list: A list of JSON-formatted carousel strings.
    """

    # Fetch the information
    info = get_info()

    # Chunk the information based on the maximum allowed items
    chunks = _chunk_info(info)

    # Process each chunk to generate carousel content
    all_carousels = [
        _generate_carousel_from_chunk(chunk)
        for chunk in chunks
    ]

    return all_carousels


def _chunk_info(info):
    """
    Splits the information into chunks of a specific size.

    Args:
        info (dict): The dictionary containing information to be chunked.

    Returns:
        list: A list of dictionaries where each dictionary is a chunk of the original info.
    """
    return [
        dict(list(info.items())[i:i + settings.MAXIMUM_ITEMS])
        for i in range(0, len(info), settings.MAXIMUM_ITEMS)
    ]


def _generate_carousel_from_chunk(chunk):
    """
    Generates a JSON-formatted carousel string for a given chunk of information.

    Args:
        chunk (dict): A chunk of information.

    Returns:
        str: JSON-formatted carousel string.
    """
    carousel = {
        "type": "carousel",
        "contents": [
            get_payload_for_bubble(instance, template.generate_bubble_string)
            for _, instance in chunk.items()
        ]
    }
    return json.dumps(carousel)


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


def send_message(api, request_type, token, messages, **kwargs):
    """
    Sends a message using the specified request type.

    Args:
    - api: The LINE bot API instance.
    - request_type: Either 'reply' or 'push'.
    - token: Token for the communication (reply_token or user_id).
    - messages: The messages to be sent.
    - **kwargs: Additional arguments for the request.

    Returns:
    - Response from the API call.
    """
    if request_type == 'reply':
        return api.reply_message(
            ReplyMessageRequest(
                reply_token=token,
                messages=messages,
                **kwargs
            )
        )
    elif request_type == 'push':
        return api.push_message(
            PushMessageRequest(
                to=token,
                messages=messages,
                **kwargs
            )
        )


def compile_message(event=None, content=None, **kwargs):
    """
    Function to push messages to LINE users.

    Args:
    - event (Event, optional): Event object containing details of the LINE event.
    - content (str, optional): The content/message to be sent.
    - **kwargs: Additional keyword arguments.

    Returns:
    - None
    """
    from main import configuration  # fix circular import
    is_task = kwargs.get('is_task', False)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # No content case: Reply with a default message if not a task.
        if not content and not is_task:
            send_message(line_bot_api, 'reply', getattr(event, 'reply_token', event),
                         [TextMessage(text='No interesting currency pairs found.')])
            return

        # Determine the request type and token based on the content and is_task flag.
        request_type = 'push' if len(content) <= settings.MAXIMUM_ITEMS or is_task else 'reply'
        token = rgetattr(event, 'source.user_id', event) if request_type == 'push' else getattr(event, 'reply_token',
                                                                                                event)

        for items in content:
            message = FlexMessage(alt_text="Overtrade Signal", contents=FlexContainer.from_json(items))
            send_message(line_bot_api, request_type, token, [message], timeout=60)
