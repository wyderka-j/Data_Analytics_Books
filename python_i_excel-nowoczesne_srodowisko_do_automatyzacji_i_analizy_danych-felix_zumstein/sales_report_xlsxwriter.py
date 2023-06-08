from pathlib import Path

import pandas as pd


# Katalog zawierający ten plik
this_dir = Path(__file__).resolve().parent

# Wczytanie wszystkich plików
parts = []
for path in (this_dir / "sales_data").rglob("*.xls*"):
    print(f'Reading {path.name}')
    part = pd.read_excel(path)
    parts.append(part)

# Połączenie obiektów DataFrame z każdego pliku w pojedynczy DataFrame
df = pd.concat(parts)

# Przestawienie każdego sklepu w kolumnę i zsumowanie wszystkich transakcji według dat
pivot = pd.pivot_table(df,
                       index="data_transakcji", columns="sklep",
                       values="kwota", aggfunc="sum")

# Resampling na koniec miesiąca i przypisanie nazwy indeksu 
summary = pivot.resample("M").sum()
summary.index.name = "Miesiąc"

# Sortowanie kolumn według przychodu ogółem
summary = summary.loc[:, summary.sum().sort_values().index]

# Dodanie wiersza i kolumny z podsumowaniem: Użycie "append" wraz z "rename"
# jest wygodnym sposobem dodania wiersza do dolnej części DataFrame.
summary.loc[:, "Razem"] = summary.sum(axis=1)
summary = summary.append(summary.sum(axis=0).rename("Razem"))

#### Zapisanie raportu zbiorczego do pliku Excela ####

# Pozycja i liczba wierszy/kolumn DataFrame.
# xlsxwriter stosuje indeksy liczone od zera.
startrow, startcol = 2, 1
nrows, ncols = summary.shape

with pd.ExcelWriter(this_dir / "sales_report_xlsxwriter.xlsx",
                    engine="xlsxwriter", datetime_format="mmm yy") as writer:
    summary.to_excel(writer, sheet_name="Arkusz1",
                     startrow=startrow, startcol=startcol)

    # Pobranie arkusza xlsxwriter i obiektu arkusza 
    book = writer.book
    sheet = writer.sheets["Arkusz1"]

    # Ustawienie tytułu
    title_format = book.add_format({"bold": True, "size": 24})
    sheet.write(0, startcol, "Raport sprzedaży", title_format)

    # Formatowanie arkusza
    # 2 = ukrycie na ekranie i wydruku
    sheet.hide_gridlines(2)

    # Formatowanie obiektu DataFrame poprzez:
    # - format liczb
    # - szerokość kolumny
    # - formatowanie warunkowe
    number_format = book.add_format({"num_format": "#,##0",
                                     "align": "center"})
    below_target_format = book.add_format({"font_color": "#E93423"})
    sheet.set_column(first_col=startcol, last_col=startcol + ncols,
                     width=14, cell_format=number_format)
    sheet.conditional_format(first_row=startrow + 1,
                             first_col=startcol + 1,
                             last_row=startrow + nrows,
                             last_col=startcol + ncols,
                             options={"type": "cell", "criteria": "<=",
                                      "value": 20000,
                                      "format": below_target_format})

    # Wykres
    chart = book.add_chart({"type": "column"})
    chart.set_title({"name": "Sprzedaż z podziałem na miesiące i sklepy"})
    chart.set_size({"width": 830, "height": 450})

    # Dodanie każdej kolumny jako serii, ignorując wiersz i kolumnę z podsumowaniem
    for col in range(1, ncols):
        chart.add_series({
             # [nazwa_akrusza, pierwszy_wiersz, pierwsza_kolumna, ostatni_wiersz, ostatnia_kolumna]
            "name": ["Arkusz1", startrow, startcol + col],
            "categories": ["Arkusz1", startrow + 1, startcol,
                           startrow + nrows - 1, startcol],
            "values": ["Arkusz1", startrow + 1, startcol + col,
                       startrow + nrows - 1, startcol + col],
        })

    # Formatowanie wykresu
    chart.set_x_axis({"name": summary.index.name,
                      "major_tick_mark": "none"})
    chart.set_y_axis({"name": "Sprzedaż",
                      "line": {"none": True},
                      "major_gridlines": {"visible": True},
                      "major_tick_mark": "none"})

    # Dodanie wykresu do arkusza
    sheet.insert_chart(startrow + nrows + 2, startcol, chart)