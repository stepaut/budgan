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
    df = df.drop(columns=[keys.PROJECT, keys.MERCHANT,
                          keys.ADDRESS, keys.NOTE, keys.TAGS, keys.AUTHOR,
                          keys.IMAGE1, keys.IMAGE2, keys.IMAGE3, keys.CURRENCY])
    df[keys.DATETIME] = df[keys.DATETIME].apply(lambda x: _parse_datetime(x))
    df[keys.DATETIME] = pd.to_datetime(df[keys.DATETIME]).astype(np.int64)
    df[keys.DATETIME] = df[keys.DATETIME].apply(lambda x: x/1000000000)
    df[keys.AMOUNT] = df[keys.AMOUNT].apply(
        lambda x: x.replace(u"\u00A0", '').replace(',', '.'))
    df[keys.AMOUNT] = df[keys.AMOUNT].astype(float)
    df[keys.CURRENCY_RATE] = df[keys.CURRENCY_RATE].apply(
        lambda x: x.replace(',', '.'))
    df[keys.CURRENCY_RATE] = df[keys.CURRENCY_RATE].astype(float)
    df[keys.AMOUNT] = df[keys.AMOUNT]*df[keys.CURRENCY_RATE]
    df = df.drop(columns=[keys.CURRENCY_RATE])

    return df
