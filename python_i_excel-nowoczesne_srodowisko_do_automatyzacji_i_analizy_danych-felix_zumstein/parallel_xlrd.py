import multiprocessing
from itertools import repeat

import xlrd
import excel


def _read_sheet(filename, sheetname):
    # Początkowy podkreślnik w nazwie funkcji jest zwyczajowo używany do 
	# oznaczenia jej jako "prywatnej", co oznacza, że nie powinna być używana
	# bezpośrednio poza tym modułem.
    with xlrd.open_workbook(filename, on_demand=True) as book:
        sheet = book.sheet_by_name(sheetname)
        data = excel.read(sheet)
    return sheet.name, data

def open_workbook(filename, sheetnames=None):
    if sheetnames is None:
        with xlrd.open_workbook(filename, on_demand=True) as book:
            sheetnames = book.sheet_names()
    with multiprocessing.Pool() as pool:
        # Domyślnie Pool tworzy tyle procesów, ile jest rdzeni procesora.
		# starmap odwzorowuje krotkę argumentów na funkcję. Wyrażenie zip
		# tworzy listę zawierającą krotki o następującej postaci:
		# [('nazwa_pliku.xlsx', 'Arkusz1'), ('nazwa_pliku.xlsx', 'Arkusz2')]
        data = pool.starmap(_read_sheet, zip(repeat(filename), sheetnames))
    return {i[0]: i[1] for i in data}
