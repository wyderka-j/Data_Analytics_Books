# Import niezbędnych pakietów
library(tidyverse)
library(psych)
library(tidymodels)

# Wczytanie danych, wybór interesujących nas kolumn
mpg <- read_csv("Dane/samochody.csv") %>% 
  select(spalanie, masa, moc, pochodzenie, liczba.cylindrów)
head(mpg)

# Statystyki opisowe
describe(mpg)

# Jednokierunkowa tabela częstości zmiennej pochodzenie
mpg %>% 
  count(pochodzenie)

# Dwukierunkowa tabela częstości
mpg %>% 
  count(pochodzenie, liczba.cylindrów) %>% 
  pivot_wider(values_from = n, names_from = liczba.cylindrów)

# Statystyki opisowe w grupach
mpg %>% 
  select(spalanie, pochodzenie) %>% 
  describeBy(group = 'pochodzenie')

# Histogram
ggplot(data = mpg, aes(x = spalanie)) +
  geom_histogram() + ylab("Liczba obserwacji")

# Wykres pudełkowy
ggplot(data = mpg, aes(x = pochodzenie,y = spalanie)) +
  geom_boxplot()

# Histogram spalania w podziale na pochodzenie
ggplot(data = mpg, aes(x = spalanie)) +
  geom_histogram() +
  facet_wrap(~ pochodzenie) + ylab("Liczba obserwacji")


# Czy istniej różnica w spalaniu?
mpg_filtered <- filter(mpg, pochodzenie == 'USA' | pochodzenie == 'Europa')

# Zmienna zależna ~ (względem) zmienna niezależna
t.test(spalanie ~ pochodzenie, data = mpg_filtered)

# Macierz korelacji
select(mpg, spalanie:moc) %>% 
  cor() 

# Wykres punktowy
ggplot(data = mpg, aes(x = masa,y = spalanie)) +
  geom_point() + xlab("Masa (funty)") +
  ylab("Spalanie (mile/galon)") + ggtitle("Związek pomiędzy masą i spalaniem")

# Wykres typu pairplot
select(mpg, spalanie:moc) %>% 
  pairs()  

# Dopasowanie linii regresji, wyświetlenie podsumowania
mpg_regression <- lm(spalanie ~ masa, data = mpg)
summary(mpg_regression)

# Wykres punktowy z linią regresji
ggplot(data = mpg, aes(x = masa, y = spalanie)) + 
  geom_point() + xlab("Masa (funty)") + 
  ylab("Spalanie (mile/galon)") + ggtitle("Związek pomiędzy masą i spalaniem") +
  geom_smooth(method = lm)

# Ziarno generatora liczb losowych
set.seed(1234)

# Podział na zbiór uczący i testowy
mpg_split <- initial_split(mpg)
mpg_train <- training(mpg_split)
mpg_test <- testing(mpg_split)

# Sprawdzenie liczby wierszy i kolumn
dim(mpg_train)
dim(mpg_test)

# Określenie rodzaju modelu treningowego
lm_spec <- linear_reg()

# Dopasowanie modelu do danych
lm_fit <- lm_spec %>%
  fit(spalanie ~ masa, data = mpg_train)

# współczynniki i wartości modelu
tidy(lm_fit)
# wskaźniki wydajności
glance(lm_fit)

# Przewidywanie wartości w zbiorze testowym 
mpg_results <- predict(lm_fit, new_data = mpg_test) %>% 
  bind_cols(mpg_test)

mpg_results

# współczynnik R-kwadrat
rsq(data = mpg_results, truth = spalanie, estimate = .pred)
# pierwiastek z błędu średniokwadratowego
rmse(data = mpg_results, truth = spalanie, estimate = .pred)
