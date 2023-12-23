import panel as pn
from bokeh.sampledata.autompg import autompg
import utils.openfilegui
import common.reading
from datetime import datetime
import holoviews as hv
import common.keys as keys
import common.analysis as al

import hvplot.pandas

pn.extension('tabulator', design='material',
             template='material', loading_indicator=True)

def main():
    file = utils.openfilegui.gui_fname("./")

    df = common.reading.get_df(file)

    expense_ = df[df[keys.K_TYPE] == keys.K_EXPENSE]
    income_ = df[df[keys.K_TYPE] == keys.K_INCOME]
    invest_ = df[(df[keys.K_TYPE] == keys.K_TRANSFER) & (
        df[keys.K_CATEGORY] == keys.K_INVESTING)]

    expenseM = al.transformByCat(expense_, 'M', keys.K_CATEGORY)
    expenseM_PC = al.transformByCat(expense_, 'M', keys.K_PARENT_CATEGORY)
    incomeM = al.transformByCat(income_, 'M', keys.K_CATEGORY)
    incomeM_PC = al.transformByCat(income_, 'M', keys.K_PARENT_CATEGORY)
    investM = al.transformByCat(invest_, 'M', keys.K_ACCOUNT_RECEIVABLE)
    totalM = al.merge(expenseM, incomeM, investM)

    expenseY = al.transformByCat(expense_, 'Y', keys.K_CATEGORY)
    expenseY_PC = al.transformByCat(expense_, 'Y', keys.K_PARENT_CATEGORY)
    incomeY = al.transformByCat(income_, 'Y', keys.K_CATEGORY)
    incomeY_PC = al.transformByCat(income_, 'Y', keys.K_PARENT_CATEGORY)
    investY = al.transformByCat(invest_, 'Y', keys.K_ACCOUNT_RECEIVABLE)
    totalY = al.merge(expenseY, incomeY, investY)

    temp = expenseM_PC.loc[:, expenseM_PC.columns != keys.K_TOTAL]
    temp.hvplot.line()

if __name__ == "__main__":
    main()