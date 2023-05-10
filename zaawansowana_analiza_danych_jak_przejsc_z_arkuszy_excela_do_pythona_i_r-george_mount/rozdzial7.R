# Wczytywanie i eksploracja danych
library(tidyverse)

# Wczytywanie danych z plików Excela
library(readxl)

# Obliczanie statystyk podsumowujących
library(psych)

# Zapis danych w formacie Excela
library(writexl)

# Funkcje z danymi i przypisywanie danych do obiektów
my_number <- 8.2
sqrt(my_number)

my_char <- 'Witaj, świecie'
toupper(my_char)

# Sprawdzenie czy obiekt jest wektorem za pomocą funkcji is.vector() i jego długości length()
is.vector(my_number)

length(my_number)

# Tworzenie wektora z wielu elementów za pomocą funkcji c()
my_numbers <- c(5, 8, 2, 7)

is.vector(my_numbers)
str(my_numbers)
length(my_numbers)

sqrt(my_numbers)

# wektor zawierajacy łańcuch znaków
roster_names <- c('Jack', 'Jill', 'Billy', 'Susie', 'Johnny')
toupper(roster_names)

# Przypisanie do tego samego wektora elementów różnego typu
my_vec <- c('A', 2, 'C')
my_vec

str(my_vec)

# Pobieranie trzeciego elementu wektora roster_names
roster_names[3]

# Pobieranie pierwszych trzech elementów z wektora
roster_names[1:3]

# Pobieranie wszystkich elementów, począwszy od drugiego aż do ostatniego
roster_names[2:length(roster_names)]

# Pobieranie drugiego i piątego elementu
roster_names[c(2, 5)]

# Utworzenie ramki danych za pomocą funkcji data.frame()
roster <- data.frame(
  imię = c('Jack', 'Jill', 'Billy', 'Susie', 'Johnny'),
  wzrost = c(182, 165, 172, 175, 168),
  ranny = c(FALSE, TRUE, FALSE, FALSE, TRUE))
roster

# Wyświetlenie listy zestawów danych instalowanych wraz z językiem R
data()

# Wyświetlenie tylko kilku pierwszych wierszy ze zbioru
head(iris)

# Potwierdzenie czy iris jest rzeczywiście ramką danych
is.data.frame(iris)

# Informacje o rozmiarze ramki danych i niektóre informacje o jej kolumnach
str(iris)

# Sprawdzenie czy pakiet psych zawiera jakieś zbiory danych
data(package = 'psych')

# Dołączenie zbioru danych sat.act z pakietu psych
data('sat.act')
str(sat.act)

# Wyświetlenie ścieżki do katalogu roboczego
getwd()

# Sprawdzenie czy uda się zlokalizować plik w folderze
file.exists('plik-testowy.csv')

file.exists('folder-testowy/plik-testowy.csv')

# TRUE jedynie w przypadku, gdy plik znajduje się o jeden folder wyżej w ścieżce
file.exists('../plik-testowy.csv')

# Wczytanie zawartości pliku .csv
read_csv('Dane/okręgi.csv')

# Przypisanie danych z pliku do obiektu
districts <- read_csv("Dane/okręgi.csv")
districts

# Importowanie danych .xlsx, .xls, .xlsm
star <- read_xlsx("Dane/star.xlsx")
head(star)

# Wyświetlenie danych w przeglądarce przypominającej arkusz kalkulacyjny w nowej karcie edytora skryptów 
View(star)

# Wyświetlenie kilku rekordów z ramki danych wraz z nazwami i typami kolumn
glimpse(star)

# Podstawowe statystyki opisowe
summary(star)

describe(star)


# Trzeci wiersz i druga kolumna ramki danych
roster[3, 2]

# Wiersze od drugiego do czwartego, kolumny od pierwszej do trzeciej
roster[2:4, 1:3]

# Tylko drugi i trzeci wiersz
roster[2:3,]

# Tylko pierwsza i trzecia kolumna
roster[, c(1,3)]

# Tylko jedna kolumna z ramki danych
roster$wzrost

is.vector(roster$wzrost)

# Zapis ramki danych roster w pliku .csv
write_csv(roster, 'dane-wyjsciowe/roster-r.csv')

# Zapis ramki danych roster w arkuszu Excela
write_xlsx(roster, 'dane-wyjsciowe/roster-r.xlsx')
