library(tidyverse)
library(readxl)
library(writexl)

# Wczytanie i połączenie danych
census <- read_csv('dane/cenzus.csv')
glimpse

divisions <- read_csv('dane/cenzus-oddziały.csv')
glimpse(divisions)

census <- left_join(census, divisions)
head(census)

# Zadanie 1. Posortuj dane rosnąco według regionu i oddziału oraz malejąco według liczby ludności. (Aby to zrobić, musisz połączyć ze sobą zbiory danych). 
#           Wyniki zapisz w arkuszu Excela.        

census %>% 
  arrange(region, oddział, desc(liczba.ludności)) %>% 
  write_xlsx("dane-wyjsciowe/cenzus-posortowane-r.xlsx")

# Zadanie 2. Usuń pole kod.pocztowy z połączonego zbioru danych.

census <- select(census, -kod.pocztowy)
head(census)

# Zadanie 3. Utwórz nową kolumnę gęstość.zaludnienia, która będzie równa liczbie ludności podzielonej przez powierzchnię.

census <- mutate(census, gęstość.zaludnienia = liczba.ludności/powierzchnia)
head(census)

# Zadanie 4. Zwizualizuj relację między powierzchnią a populacją dla wszystkich obserwacji z 2015 roku.

census_2015 <- filter(census, rok == 2015)

ggplot(data = census_2015, aes(x = powierzchnia, y = liczba.ludności))+
  geom_point()

# Zadanie 5. Znajdź całkowitą liczbę ludności w każdym regionie w 2015 roku.

census_2015 %>% 
  group_by(region) %>% 
  summarise(ttl_liczba.ludności = sum(liczba.ludności))

# Zadanie 6. Utwórz tabelę zawierającą nazwy stanów i liczbę ludności, w której liczba ludności z każdego roku od 2010 do 2015 przechowywana jest w osobnej kolumnie.

pivot_wider(data = select(census, c('stan','rok','liczba.ludności')), 
            names_from = 'rok', values_from = 'liczba.ludności')
