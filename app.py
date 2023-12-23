import panel as pn
import hvplot.pandas
import pandas as pd
from bokeh.sampledata.autompg import autompg
import utils.openfilegui
import common.reading
from datetime import datetime
import holoviews as hv
import common.keys as keys
import common.analysis as al

pn.extension(design='material')

file = utils.openfilegui.gui_fname("./")

df = common.reading.get_df(file)

expense_ = df[df[keys.TYPE] == keys.EXPENSE]
income_ = df[df[keys.TYPE] == keys.INCOME]
invest_ = df[(df[keys.TYPE] == keys.TRANSFER) & (
    df[keys.CATEGORY] == keys.INVESTING)]

expenseM = al.transformByCat(expense_, 'M', keys.CATEGORY)
expenseM_PC = al.transformByCat(expense_, 'M', keys.PARENT_CATEGORY)
incomeM = al.transformByCat(income_, 'M', keys.CATEGORY)
incomeM_PC = al.transformByCat(income_, 'M', keys.PARENT_CATEGORY)
investM = al.transformByCat(invest_, 'M', keys.ACCOUNT_RECEIVABLE)
totalM = al.merge(expenseM, incomeM, investM)

expenseY = al.transformByCat(expense_, 'Y', keys.CATEGORY)
expenseY_PC = al.transformByCat(expense_, 'Y', keys.PARENT_CATEGORY)
incomeY = al.transformByCat(income_, 'Y', keys.CATEGORY)
incomeY_PC = al.transformByCat(income_, 'Y', keys.PARENT_CATEGORY)
investY = al.transformByCat(invest_, 'Y', keys.ACCOUNT_RECEIVABLE)
totalY = al.merge(expenseY, incomeY, investY)


expenseM_PC_p = expenseM_PC.loc[:, expenseM_PC.columns !=
                       keys.TOTAL].hvplot.line()
incomeM_PC_p = incomeM_PC.loc[:, incomeM_PC.columns !=
                                   keys.TOTAL].hvplot.line()

selector = pn.widgets.Select(name='Select', options=[
                           keys.EXPENSE, keys.INCOME])

pn.Column(expenseM_PC_p, incomeM_PC_p).servable()
