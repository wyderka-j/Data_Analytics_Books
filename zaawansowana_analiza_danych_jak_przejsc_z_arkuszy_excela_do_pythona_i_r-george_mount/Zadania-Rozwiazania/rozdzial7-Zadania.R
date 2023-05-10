# Zadanie 1. Utwórz wektor znaków składający się z pięciu elementów, a następnie uzyskaj dostęp do pierwszego i czwartego elementu tego wektora.

# pięcioelementowy wektor łańcuchów znaków
my_strings <- c('Życzę', 'Ci', 'ba"R"dzo', 'miłego', 'dnia')

# dostęp do 1 i 4 elementu wektora
my_strings[c(1,4)]

# Zadanie 2. Utwórz dwa wektory, x i y, o długości 4. Pierwszy ma zawierać wartości liczbowe, a drugi logiczne. Pomnóż je i zapisz rezultat w obiekcie z. 
# Jaki wynik otzrymałeś?

x <- c(1, 2, 3, 4)
y <- c(TRUE, FALSE, TRUE, FALSE)
z <- x * y
z
### Wartości logiczne zostały zamienione na liczby, którymi są w rzeczywistości.

# Zadanie 3. Z repozytorium CRAN pobierz pakiet nycflights13. Ile zbiorów danych znajduje się w tym pakiecie?
# a) Jeden ze zbiorów nazywa się airports. Wyświetl kilka pierwszych wierszy z jego ramki danych oraz oblicz statystyki opisowe.
# b) W pakiecie znajdziesz też zbiór weather. Wybierz z ramki danych wiersze od 10 do 12 i kolumny od 4 do 7. Zapisz wyniki w pliku .csv i arkuszu Excela.

# install.packages('nycflights13')
library(nycflights13)
data(package = 'nycflights13')
### 5 zbiorów danych

# kilka pierwszych wierszy z jego ramki danych oraz statystyki opisowe
data('airports')

head(airports)
summary(airports)

# zbiór weather
data('weather')

weather_subset <- weather[10:12, 4:7]

library(tidyverse)
write_csv(weather_subset, 'dane-wyjsciowe/weather_podzbiór.csv')

library(writexl)
write_xlsx(weather_subset, 'dane-wyjsciowe/weather_podzbiór.xlsx')
