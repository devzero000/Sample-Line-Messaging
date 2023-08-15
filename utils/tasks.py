import json

import requests
from firebase_admin import firestore

import config.api as api
import config.settings as settings
import flex.template as template
import utils.functions as func


def task_set_keep_alive_web_server():
    requests.get(api.WEBSERVER)


def task_alert_trade():
    data = func.get_info(is_task=True)
    forex_entries = data.get('data', [])

    if not forex_entries:
        return {'error': 'Data not found!'}

    forex_info = _extract_forex_info(forex_entries)

    # Breaking down the info into chunks of 12
    chunks = _split_into_chunks(forex_info, settings.MAXIMUM_ITEMS)

    all_carousels = [
        json.dumps({
            "type": "carousel",
            "contents": [template.alert_indicator(instance) for _, instance in chunk.items()]
        })
        for chunk in chunks
    ]

    func.compile_message(settings.ADMIN_ID, all_carousels, is_task=True)


def _extract_forex_info(forex_entries):
    from main import app
    db = firestore.client()
    doc_ref = db.collection('settings').document('INDICATOR')
    fb_config = doc_ref.get().to_dict()

    forex_info = {}
    alert_value = fb_config.get('maximum_indicator', settings.ALERT_VALUE_INDICATOR)
    app.logger.info(f'Alert Value: {alert_value}')

    for entry in forex_entries:
        currency = entry.get('s')
        indicator = entry.get('d')[:8]

        is_overbought = sum(1 for x in indicator if x >= settings.OVERBOUGHT)
        is_oversold = sum(1 for x in indicator if x <= settings.OVERSOLD)

        if is_overbought >= alert_value or is_oversold >= alert_value:
            name, desc, _, _ = func.get_currency_pair_description(currency)
            forex_info[name] = {
                'symbol': name,
                'signal': '⬇' if is_overbought > is_oversold else '⬆',
                'description': desc,
            }

    return forex_info


def _split_into_chunks(data, max_items):
    return [dict(list(data.items())[i:i + max_items]) for i in range(0, len(data), max_items)]
