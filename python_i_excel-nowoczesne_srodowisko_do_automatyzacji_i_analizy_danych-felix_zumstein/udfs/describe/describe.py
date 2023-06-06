import xlwings as xw
import pandas as pd


@xw.func
@xw.arg("df", pd.DataFrame)
def describe(df, selection=None):
    if selection is not None:
        return df.loc[:, selection].describe()
    else:
        return df.describe()