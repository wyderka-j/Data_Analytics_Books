# Wczytanie bibliotek
library(tidyverse)
library(readxl)

# Wczytanie danych
star <- read_excel("dane/star.xlsx")
head(star)

# Wybór kolumn ze zbioru star
select(star, wynik.matematyka, wynik.czytanie, id.szkoły)

# Pominięcie kolumn
select(star, -wynik.matematyka, -wynik.czytanie, -id.szkoły)

select(star, -c(wynik.matematyka, wynik.czytanie, id.szkoły))

# Wybór wszystkich kolumn od wynik.matematyka do doświadczenie.nauczyciela;
# Przypisanie wyniku do obiektu star
star <- select(star, wynik.matematyka:doświadczenie.nauczyciela)
head(star)

# Obliczanie łącznego wyniku
star <- mutate(star, nowa_kolumna = wynik.matematyka + wynik.czytanie)
head(star)

# Zmiana nazwy
star <- rename(star, łączny.wynik = nowa_kolumna)
head(star)

# Sortowanie
arrange(star, rodzaj.klasy, wynik.czytanie)

# Sortowanie malejąco według kolumny rodzaj.klasy i rosnąco według kolumny wynik.czytanie
arrange(star, desc(rodzaj.klasy), wynik.czytanie)

# Filtrowanie
filter(star, rodzaj.klasy == 'mała.klasa')

filter(star, wynik.czytanie >= 500)

# Pobieramy rekordy dotyczące małych klas, w których wynik.czytanie wynosi co najmniej 500 
filter(star, rodzaj.klasy == 'mała.klasa' & wynik.czytanie >= 500)

# Grupowanie
star_grouped <- group_by(star, rodzaj.klasy)
head(star_grouped)

# Średni wynik z matematyki w zależności od rozmiaru klasy
summarize(star_grouped, średnia.z.matematyki = mean(wynik.matematyka))


# Wczytywanie danych
star <- read_excel('dane/star.xlsx')
head(star)

districts <- read_csv('dane/okręgi.csv')
head(districts)

# Złączenie lewostronne zewnętrzne tabel star i districts
left_join(select(star, id.szkoły, wynik.matematyka, wynik.czytanie), districts)

# Średnie wyniki testu z czytania w poszczególnych radzajach klas posortowane malejaco
star_grouped <- group_by(star, rodzaj.klasy)
star_avg_reading <- summarize(star_grouped, średnia.z.czytania = mean(wynik.czytanie))
star_avg_reading_sorted <- arrange(star_avg_reading, desc(średnia.z.czytania))
star_avg_reading_sorted  

# Użycie %>% 
# Średni wynik z czytania w zależności od klasy
# posortowany od najwyższego do najniższego

star %>% 
  group_by(rodzaj.klasy) %>%
  summarise(średnia.z.czytania = mean(wynik.czytanie)) %>% 
  arrange(desc(średnia.z.czytania))

# Średnia z czytania i matematyki w każdym okręgu
star %>% 
  group_by(id.szkoły) %>% 
  summarise(średnia.z.czytania = mean(wynik.czytanie), średnia.z.matematyki = mean(wynik.matematyka)) %>% 
  arrange(id.szkoły) %>% 
  head()

# Przekształcanie danych za pomocą tidyr
# dodanie kolumny z indeksem row_number()
star_pivot <- star %>% 
  select(c(id.szkoły, wynik.czytanie, wynik.matematyka)) %>% 
  mutate(id = row_number())


star_long <- star_pivot %>% 
  pivot_longer(cols = c(wynik.matematyka, wynik.czytanie),
               values_to = 'wynik', names_to = 'rodzaj.testu')


head(star_long)
# Zmiana nazwy wynik.matematyka i wynik.czytanie na matematyka i czytanie
star_long <- star_long %>%
  mutate(rodzaj.testu = recode(rodzaj.testu, 
                               'wynik.matematyka' = 'matematyka', 'wynik.czytanie' = 'czytanie')) 

distinct(star_long, rodzaj.testu)

# ponowne rozszerzenie ramki
star_wide <- star_long %>% 
  pivot_wider(values_from = 'wynik', names_from = 'rodzaj.testu') 
head(star_wide)


# Wykres liczności
ggplot(data = star,
       aes(x = rodzaj.klasy))+
  geom_bar()

# Histogram
ggplot(data = star,aes(x = wynik.czytanie))+
  geom_histogram()

# histogram- zmiana koloru
ggplot(data = star, aes(x = wynik.czytanie))+
  geom_histogram(bins = 25, fill = 'pink')

# Wykres pudełkowy
ggplot(data = star,aes(x = wynik.czytanie))+
  geom_boxplot()

# Obrócony wykres pudełkowy
ggplot(data = star, aes(y = wynik.czytanie))+
  geom_boxplot()

# Zgrupowany wykres pudełkowy
ggplot(data = star, aes(x = rodzaj.klasy,y = wynik.czytanie))+
  geom_boxplot()

# Wykres punktowy
ggplot(data=star,aes(x = wynik.matematyka,y = wynik.czytanie))+
  geom_point()

# Wykres punktowy z wlasnymi nazwami osi i tytułem
ggplot(data = star, aes(x = wynik.matematyka, y = wynik.czytanie))+
  geom_point() + 
  xlab('Wynik z matematyki') + ylab('Wynik z czytania')+
  ggtitle('Wyniki z matematyki i czytania')
