import multiprocessing
from itertools import repeat

import pandas as pd
import openpyxl


def _read_sheet(filename, sheet_name):
    # Początkowy podkreślnik w nazwie funkcji jest zwyczajowo używany do 
	# oznaczenia jej jako "prywatnej", co oznacza, że nie powinna być używana
	# bezpośrednio poza tym modułem.
    df = pd.read_excel(filename, sheet_name=sheet_name, engine='openpyxl')
    return sheet_name, df

def read_excel(filename, sheet_name=None):
    if sheet_name is None:
        book = openpyxl.load_workbook(filename,
                                      read_only=True, data_only=True)
        sheet_name = book.sheetnames
        book.close()
    with multiprocessing.Pool() as pool:
        # Domyślnie Pool tworzy tyle procesów, ile jest rdzeni procesora.
		# starmap odwzorowuje krotkę argumentów na funkcję. Wyrażenie zip
		# tworzy listę zawierającą krotki o następującej postaci:
		# [('nazwa_pliku.xlsx', 'Arkusz1'), ('nazwa_pliku.xlsx', 'Arkusz2')]
        data = pool.starmap(_read_sheet, zip(repeat(filename), sheet_name))
    return {i[0]: i[1] for i in data}
