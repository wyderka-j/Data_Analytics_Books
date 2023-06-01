from pathlib import Path

import pandas as pd


# Katalog zawierający ten plik
this_dir = Path(__file__).resolve().parent

# Wczytanie wszystkich plików Excela z wszystkich podfolderów w sales_data
parts = []
for path in (this_dir / "sales_data").rglob("*.xls*"):
    print(f'Reading {path.name}')
    part = pd.read_excel(path, index_col="id_transakcji")
    parts.append(part)

# Połączenie obiektów DataFrame z każdego pliku w pojedynczy DataFrame
# pandas zadba o prawidłowe wyrównanie kolumn
df = pd.concat(parts)

# Przestawienie każdego sklepu w kolumnę i zsumowanie wszystkich transakcji według dat
pivot = pd.pivot_table(df,
                       index="data_transakcji", columns="sklep",
                       values="kwota", aggfunc="sum")

# Resampling na koniec miesiąca i przypisanie nazwy indeksu
summary = pivot.resample("M").sum()
summary.index.name = "Miesiąc"

# Zapisanie raportu zbiorczego do pliku Excela
summary.to_excel(this_dir / "sales_report_pandas.xlsx")
