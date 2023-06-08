from pathlib import Path

import pandas as pd
import xlwings as xw


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

# Otwarcie szablonu, wklejenie danych, automatyczne dopasowanie kolumn 
# i dostosowanie źródła wykresu. Następnie zapisanie go pod inną nazwą.
template = xw.Book(this_dir / "xl" / "sales_report_template.xlsx")
sheet = template.sheets["Arkusz1"]
sheet["B3"].value = summary
sheet["B3"].expand().columns.autofit()
sheet.charts["Wykres 1"].set_source_data(sheet["B3"].expand()[:-1, :-1])
template.save(this_dir / "sales_report_xlwings.xlsx")