from functools import lru_cache

import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import xlwings as xw


@lru_cache()
@xw.func(call_in_wizard=False)
@xw.arg("mids", doc="Identyfikatory MID: zakres maksymalnie 5 komórek")
@xw.arg("start_date", doc="Komórka sformatowana jako data")
@xw.arg("end_date", doc="Komórka sformatowana jako data")
def get_interest_over_time(mids, start_date, end_date):
    """Zapytanie do Google Trends - zastępuje identyfikatory mid
    popularnych języków programowania ich odpowiednikami czytelnymi
    dla człowieka w zwracanej wartości, np. zamiast "/m/05z1_"
    zwraca "Python".
    """
    mids = mids.value

    # Sprawdzanie i przekształcanie parametrów
    assert len(mids) <= 5, "Zbyt wiele identyfikatorów mid (maksymalnie: 5)"
    start_date = start_date.date().isoformat()
    end_date = end_date.date().isoformat()

    # Wykonanie zapytania do Google Trends i zwrócenie DataFrame
    trend = TrendReq(timeout=10)
    trend.build_payload(kw_list=mids,
                        timeframe=f"{start_date} {end_date}")
    df = trend.interest_over_time()

    # Zastąpienie identyfikatorów mid słowem zrozumiałym dla człowieka
    mids = {"/m/05z1_": "Python", "/m/02p97": "JavaScript",
            "/m/0jgqg": "C++", "/m/07sbkfb": "Java", "/m/060kv": "PHP"}
    df = df.rename(columns=mids)

    #  Usunięcie kolumny isPartial
    return df.drop(columns="isPartial")


@xw.func
@xw.arg("df", pd.DataFrame)
def plot(df, name, caller):
    plt.style.use("seaborn")
    if not df.empty:
        caller.sheet.pictures.add(df.plot().get_figure(),
                                  top=caller.offset(row_offset=1).top,
                                  left=caller.left,
                                  name=name, update=True)
    return f"<Plot: {name}>"


if __name__ == "__main__":
    xw.serve()
