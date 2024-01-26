import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime
import holoviews as hv
from . import keys


def transformByCat(data: pd.DataFrame, level: str, col_name: str) -> pd.DataFrame:
    s = data[keys.DATETIME].min()
    e = data[keys.DATETIME].max()
    start_date = datetime.fromtimestamp(s)
    end_date = datetime.fromtimestamp(e)
    
    if level == "M":
        date_mode = "%m-%Y"
    elif level == "Y":
        date_mode = "%Y"
    elif level == "Q":
        raise NotImplementedError()  # TODO quarter
    else:
        raise Exception()

    unique_cats = data[col_name].unique()
    data_by_cat = pd.DataFrame(columns=unique_cats)

    el_list = pd.period_range(start=start_date, end=end_date, freq=level)
    el_list = [el.strftime(date_mode) for el in el_list]
    data_by_cat[keys.INDEX] = el_list
    data_by_cat = data_by_cat.set_index(keys.INDEX)

    for col in data_by_cat.columns:
        data_by_cat[col].values[:] = 0

    for index, row in data.iterrows():
        date = datetime.fromtimestamp(row[keys.DATETIME])
        el = date.strftime(date_mode)
        cat = row[col_name]
        value = row[keys.AMOUNT]
        data_by_cat.loc[data_by_cat.index == el, cat] += abs(value)

    data_by_cat[keys.TOTAL] = data_by_cat.sum(axis=1)

    return data_by_cat


def merge(expense: pd.DataFrame, income: pd.DataFrame, invest: pd.DataFrame):
    result = pd.DataFrame(index=expense.index)
    result[keys.EXPENSE] = expense[keys.TOTAL]
    result[keys.INCOME] = income[keys.TOTAL]
    result[keys.INVESTING] = invest[keys.TOTAL]
    result[keys.TOTAL] = result[keys.INCOME] - \
        result[keys.EXPENSE] - result[keys.INVESTING]
    result[keys.TOTAL] = result[keys.TOTAL].cumsum()

    result[keys.EXPENSE_SHARE] = result[keys.EXPENSE] / \
        result[keys.INCOME] * 100
    result[keys.INVESTING_SHARE] = result[keys.INVESTING] / \
        result[keys.INCOME] * 100
    return result


def getDFForPie(data: pd.DataFrame, year: str, limit=5):
    df = data.T.drop(index=keys.TOTAL)
    df = df[[year]]
    df = df.loc[~(df == 0).all(axis=1)]
    sum = df[year].sum()
    if sum == 0:
        return None
    df[year] = df[year]/sum*100
    df.loc[keys.OTHER] = 0
    df[keys.TEMP] = False
    for index, row in df.iterrows():
        if row[year] < limit:
            df.loc[keys.OTHER, year] += row[year]
            df.loc[index, keys.TEMP] = True
    df.loc[keys.OTHER, keys.TEMP] = False
    df = df.drop(df[df[keys.TEMP]].index)
    df = df.drop(columns=keys.TEMP)

    return df


def get_most_changed(data: pd.DataFrame, year: float, min_sign_proc: float = 0.03) -> pd.DataFrame:
    df = data.copy()
    df.index = df.index.astype('int')
    previous = year - 1
    df = df[df.index.isin([previous, year])]
    df = df.drop(columns=(keys.TOTAL))
    total = df.loc[year].sum()
    df = df.loc[:, (df > total * min_sign_proc).any()]
    df = df.loc[:, (df > 0).all()]
    df = df.transpose()
    df[keys.INCREASE] = (df[year] - df[previous])/df[previous] * 100
    df[keys.INCREASE] = df[keys.INCREASE].astype('int')
    df = df.sort_values(by=[keys.INCREASE], ascending=False)
    return df


# def makePies(data: pd.DataFrame):
#     years = len(data.T.columns)
#     # fig, axes = plt.subplots(nrows=len(data.T.columns), figsize=(30,30))
#     for year_num in range(years):
#         year = data.T.columns[year_num]
#         df = getDFForPie(data, year, 2)
#         if df is None:
#             continue
#         # df.plot(ax=axes[year_num], kind='pie', autopct='%i%%', y=year, legend=False, subplots=True)
#         plt.figure(figsize=(40, 40))
#         df.plot(kind='pie', autopct='%i%%',
#                 y=year, legend=False, subplots=True)


# def make_single_lines(data: pd.DataFrame):
#     data = data.loc[:, data.columns != keys.K_TOTAL]
#     for c in data.columns:
#         df = data[c]

#         plt.figure(figsize=(6, 6))
#         plt.title(c)
#         plt.grid(True)
#         df.plot(subplots=True)


# map: (name,type)
def get_df_mapped(data: pd.DataFrame, map: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df = df.drop(columns=df.columns)

    for t in map['type'].unique():
        df[t] = 0

    for c in data.columns:
        if c == keys.TOTAL:
            continue
        ii = map.loc[map['name'] == c]
        if len(ii) == 0:
            continue
        row = ii.index[0]
        t = map['type'][row]
        df[t] += data[c]

    for c in df.columns:
        df[c] = df[c].cumsum()

    df = df.loc[:, (df != 0).any(axis=0)]
    df = df.loc[~(df == 0).all(axis=1)]

    return df
