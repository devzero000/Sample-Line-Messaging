import config.settings as settings
from utils import timezone


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
                            "backgroundColor": "#2edb02" if float(value) >= settings.OVERBOUGHT else "#ff2424",
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


def alert_indicator(info):
    signal_buy = bool(info['signal'] == '⬆')

    template = {
        "type": "bubble",
        "size": "mega",
        "header": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": info['symbol'],
                                    "color": "#ffffff",
                                    "size": "xl",
                                    "flex": 4,
                                    "weight": "bold"
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": info['description'],
                                    "color": "#ffffff66",
                                    "size": "sm"
                                }
                            ]
                        },
                    ],
                    "margin": "sm",
                    "flex": 3
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "image",
                            "url": settings.ICON_UP if signal_buy else settings.ICON_DOWN,
                            "size": "xxs",
                            "margin": "md"
                        }
                    ],
                    "alignItems": "flex-end"
                }
            ],
            "paddingAll": "20px",
            "backgroundColor": "#0367D3" if signal_buy else "#d61e34",
            "spacing": "xs",
            "height": "100px",
            "paddingTop": "22px"
        }
    }
    return template
