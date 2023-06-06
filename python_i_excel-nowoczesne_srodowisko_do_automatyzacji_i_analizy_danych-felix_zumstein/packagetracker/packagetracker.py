"""Moduł ten zawiera wszystkie funkcje, które są wywoływane z Excela
lub operują na Excelu.
"""

import datetime as dt

from dateutil import tz
import requests
import pandas as pd
import matplotlib.pyplot as plt
import xlwings as xw

import database


# Jest to część adresu URL, która jest taka sama dla każdego żądania
BASE_URL = "https://pypi.org/pypi"


def add_package():
    """ Dodaje do bazy danych nowy pakiet wraz z historią wersji.
    Wywołuje aktualizację listy rozwijanej na karcie Tropiciel.
    """
    # Obiekty Excela
    db_sheet = xw.Book.caller().sheets["Baza danych"]
    package_name = db_sheet["new_package"].value
    feedback_cell = db_sheet["new_package"].offset(column_offset=1)

    # Wyczyszczenie komórek z informacjami zwrotnymi
    feedback_cell.clear_contents()

    # Sprawdzenie, czy pakiet istnieje na PyPI
    if not package_name:
        feedback_cell.value = "Błąd: proszę podać nazwę!"
        return
    if requests.get(f"{BASE_URL}/{package_name}/json",
                    timeout=6).status_code != 200:
        feedback_cell.value = "Błąd: nie znaleziono pakietu!"
        return

    # Wprowadzenie nazwy pakietu do tabeli packages.
    error = database.store_package(package_name)
    db_sheet["new_package"].clear_contents()

    # Wyświetlenie ewentualnych błędów lub uruchomienie aktualizacji bazy danych
    # i odświeżenie listy rozwijanej, aby można było wybrać nowy pakiet.
    if error:
        feedback_cell.value = f"Błąd: {error}"
    else:
        feedback_cell.value = f"Pomyślnie dodano {package_name}."
        update_database()
        refresh_dropdown()


def update_database():
    """ Usunięcie wszystkich rekordów z tabeli z wersjami, ponowne pobranie
        wszystkich danych z PyPI i ponowne zapisanie wersji w tabeli.
    """
    # Obiekty Excela
    sheet_db = xw.Book.caller().sheets["Baza danych"]

    # Wyczyszczenie dzienników
    sheet_db["log"].expand().clear_contents()

    # Generalne porządki: usunięcie wszystkich wersji wszystkich
    # pakietów i ponowne wypełnienie tabeli package_versions od zera
    database.delete_versions()
    df_packages = database.get_packages()
    logs = []

    # Zapytanie do API REST PyPI
    for package_id, row in df_packages.iterrows():
        ret = requests.get(f"{BASE_URL}/{row['package_name']}/json",
                           timeout=6)
        if ret.status_code == 200:
            ret = ret.json()  # przekształcenie łańcucha JSON w słownik
            logs.append(f"INFO: pomyślnie pobrano {row['package_name']}")
        else:
            logs.append(f"BŁĄD: Nie można pobrać danych dla {row['package_name']}")
            continue

        # Utworzenie instancji obiektu DataFrame poprzez pobranie danych z odpowiedzi API REST 
        releases = []
        for version, files in ret["releases"].items():
            if ret["releases"][version]:  # ignorowanie wydań bez informacji
                releases.append((files[0]["upload_time"], version, package_id))
        df_releases = pd.DataFrame(columns=["uploaded_at", "version_string", "package_id"],
                                   data=releases)
        df_releases["uploaded_at"] = pd.to_datetime(df_releases["uploaded_at"])
        df_releases = df_releases.sort_values("uploaded_at")
        database.store_versions(df_releases)
        logs.append(f"INFO: {row['package_name']} został pomyślnie zapisany w bazie danych")

    # Wypisanie ostatnio zaktualizowanego znacznika czasu i zapisów dziennika
    sheet_db["updated_at"].value = (f"Ostatnia aktualizacja: "
                                    f"{dt.datetime.now(tz.UTC).isoformat()}")
    sheet_db["log"].options(transpose=True).value = logs


def show_history():
    """ Wyświetla najnowsze wydanie i historię wydań
    (liczba wydań w ciągu roku)
    """
    # Obiekty Excela
    book = xw.Book.caller()
    tracker_sheet = book.sheets["Tropiciel"]
    package_name = tracker_sheet["package_selection"].value
    feedback_cell = tracker_sheet["package_selection"].offset(column_offset=1)
    picture_cell = tracker_sheet["latest_release"].offset(row_offset=2)

    # Użycie stylu "seaborn" dla wykresów Matplotlib wytworzonych przez pandas
    plt.style.use("seaborn")

    # Sprawdzenie danych wejściowych
    if not package_name:
        feedback_cell.value = ("Błąd: proszę najpierw wybrać pakiet! "
                               "Najpierw musisz dodać jakiś pakiet do bazy danych.")
        return

    # Wyczyszenie komórek wyjściowych i rysunku
    feedback_cell.clear_contents()
    tracker_sheet["latest_release"].clear_contents()
    if "releases_per_year" in tracker_sheet.pictures:
        tracker_sheet.pictures["releases_per_year"].delete()

    # Pobranie wszystkich wersji pakietu z bazy danych
    try:
        df_releases = database.get_versions(package_name)
    except Exception as e:
        feedback_cell.value = repr(e)
        return
    if df_releases.empty:
        feedback_cell.value = f"Błąd: Nie znaleziono żadnych wydań dla {package_name}"
        return

    # Obliczenie liczby wydań w ciągu roku i sporządzenie wykresu
    df_releases_yearly = df_releases.resample("Y").count()
    df_releases_yearly.index = df_releases_yearly.index.year
    df_releases_yearly.index.name = "Lata"
    df_releases_yearly = df_releases_yearly.rename(
        columns={"version_string": "Liczba wydań"})
    ax = df_releases_yearly.plot.bar(
        title=f"Liczba wydań na rok "
              f"({tracker_sheet['package_selection'].value})")

    # Zapisanie wyników i wykresu do Excela
    version = df_releases.loc[df_releases.index.max(), "version_string"]
    tracker_sheet["latest_release"].value = (
        f"{version} ({df_releases.index.max():%d.%m.%Y} r.)")
    tracker_sheet.pictures.add(ax.get_figure(), name="releases_per_year",
                               top=picture_cell.top,
                               left=picture_cell.left)


def refresh_dropdown():
    """ Odświeżenie listy rozwijanej na karcie Tropiciel o zawartość
	tabeli packages.
    """
    # Obiekty Excela
    book = xw.Book.caller()
    dropdown_sheet = book.sheets["Lista rozwijana"]
    tracker_sheet = book.sheets["Tropiciel"]

    # Wyczyszczenie aktualnej wartości na liście rozwijanej
    tracker_sheet["package_selection"].clear_contents()

    # Jeśli tabela w Excelu zawiera niepuste wiersze, zostaną one usunięte
	# przed ponownym wypełnieniem jej wartościami z tabeli bazy danych packages
    if dropdown_sheet["dropdown_content"].value:
        dropdown_sheet["dropdown_content"].delete()
    dropdown_sheet["dropdown_content"].options(
        header=False, index=False).value = database.get_packages()


if __name__ == "__main__":
    xw.Book("packagetracker.xlsm").set_mock_caller()
    add_package()
