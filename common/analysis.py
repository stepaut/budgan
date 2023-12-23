import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime
import holoviews as hv
from . import keys


def transformByCat(data: pd.DataFrame, level: str, col_name: str) -> pd.DataFrame:
    start_date = datetime.fromtimestamp(data[keys.K_DATETIME].min())
    end_date = datetime.fromtimestamp(data[keys.K_DATETIME].max())
    
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
    data_by_cat[keys.K_INDEX] = el_list
    data_by_cat = data_by_cat.set_index(keys.K_INDEX)

    for col in data_by_cat.columns:
        data_by_cat[col].values[:] = 0

    for index, row in data.iterrows():
        date = datetime.fromtimestamp(row[keys.K_DATETIME])
        el = date.strftime(date_mode)
        cat = row[col_name]
        value = row[keys.K_AMOUNT]
        data_by_cat.loc[data_by_cat.index == el, cat] += abs(value)

    data_by_cat[keys.K_TOTAL] = data_by_cat.sum(axis=1)

    return data_by_cat


def merge(expense: pd.DataFrame, income: pd.DataFrame, invest: pd.DataFrame):
    result = pd.DataFrame(index=expense.index)
    result[keys.K_EXPENSE] = expense[keys.K_TOTAL]
    result[keys.K_INCOME] = income[keys.K_TOTAL]
    result[keys.K_INVESTING] = invest[keys.K_TOTAL]
    result[keys.K_TOTAL] = result[keys.K_INCOME] - \
        result[keys.K_EXPENSE] - result[keys.K_INVESTING]
    result[keys.K_TOTAL] = result[keys.K_TOTAL].cumsum()

    result[keys.K_EXPENSE_SHARE] = result[keys.K_EXPENSE] / \
        result[keys.K_INCOME] * 100
    result[keys.K_INVESTING_SHARE] = result[keys.K_INVESTING] / \
        result[keys.K_INCOME] * 100
    return result


def getDFForPie(data: pd.DataFrame, year: str, limit=5):
    df = data.T.drop(index=keys.K_TOTAL)
    df = df[[year]]
    df = df.loc[~(df == 0).all(axis=1)]
    sum = df[year].sum()
    if sum == 0:
        return None
    df[year] = df[year]/sum*100
    df.loc[keys.K_OTHER] = 0
    df[keys.K_TEMP] = False
    for index, row in df.iterrows():
        if row[year] < limit:
            df.loc[keys.K_OTHER, year] += row[year]
            df.loc[index, keys.K_TEMP] = True
    df.loc[keys.K_OTHER, keys.K_TEMP] = False
    df = df.drop(df[df[keys.K_TEMP]].index)
    df = df.drop(columns=keys.K_TEMP)

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
