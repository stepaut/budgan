import pandas as pd
from . import keys
from datetime import datetime
import numpy as np


def _parse_datetime(x: str):
    rus = {"янв": "jan",
           "февр": "feb", "фев": "feb",
           "мар": "mar",
           "апр": "apr",
           "май": "may", "мая": "may",
           "июн": "jun",
           "июл": "jul",
           "авг": "aug",
           "сент": "sep", "сен": "sep",
           "окт": "oct",
           "нояб": "nov", "ноя": "nov",
           "дек": "dec",
           "г. ": "",
           ".": ""}
    for r, e in rus.items():
        x = x.lower().replace(r, e)
    try:
        dt = datetime.strptime(x.lower(), u'%d %b %Y %H:%M:%S')
    except:
        dt = datetime.strptime(x.lower(), u'%d%m%Y %H:%M:%S')
    return dt


def get_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, on_bad_lines="warn", sep="\t")
    df = df.drop(columns=[keys.K_PROJECT, keys.K_ACCOUNT, keys.K_PAYMENT_ACCOUNT, keys.K_MERCHANT,
                          keys.K_ADDRESS, keys.K_NOTE, keys.K_TAGS, keys.K_AUTHOR,
                          keys.K_IMAGE1, keys.K_IMAGE2, keys.K_IMAGE3, keys.K_CURRENCY])
    df[keys.K_DATETIME] = df[keys.K_DATETIME].apply(lambda x: _parse_datetime(x))
    df[keys.K_DATETIME] = pd.to_datetime(df[keys.K_DATETIME]).astype(np.int64)
    df[keys.K_DATETIME] = df[keys.K_DATETIME].apply(lambda x: x/1000000000)
    df[keys.K_AMOUNT] = df[keys.K_AMOUNT].apply(
        lambda x: x.replace(u"\u00A0", '').replace(',', '.'))
    df[keys.K_AMOUNT] = df[keys.K_AMOUNT].astype(float)
    df[keys.K_CURRENCY_RATE] = df[keys.K_CURRENCY_RATE].apply(
        lambda x: x.replace(',', '.'))
    df[keys.K_CURRENCY_RATE] = df[keys.K_CURRENCY_RATE].astype(float)
    df[keys.K_AMOUNT] = df[keys.K_AMOUNT]*df[keys.K_CURRENCY_RATE]
    df = df.drop(columns=[keys.K_CURRENCY_RATE])

    return df
