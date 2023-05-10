#install.packages('DAAG')
library(DAAG)
library(tidyverse)
library(tidymodels)
library(readxl)

ais <- read_excel("dane/ais.xlsx")

# Zadanie 1. Zwizualizuj rozkład liczby czerwonych krwinek (rcc) według płci (płeć).

ggplot(data = ais, aes(x = rcc))+
  geom_histogram()+
  facet_wrap(~ płeć)

# Zadanie 2. Czy istnieje znacząca różnica w liczbie czerwonych krwinek między tymi grupami?

t.test(rcc ~ płeć, data=ais)
# Tak, istnieje statystycznie istotna różnica

# Zadanie 3. Utwórz macierz korelacji odpowiednich zmiennych.

ais %>% 
  select(-c(płeć, sport)) %>% 
  cor()

# Zadanie 4. Zwizualizuj związek wzrostu (wzrost) z wagą (waga).

ggplot(data = ais, aes(x = wzrost,y = waga))+
  geom_point()

# Zadanie 5. Za pomocą regresji liniowej znajdź zależność wzrostu od wagi. Znajdź równanie prostej regresji. Czy istnieje znaczący związek między parametrami?
#            Jaki procent zmienności wzrstu wyaźnia waga?

# Regresja: waga w zależności od wzrostu
ais_reg <- lm(waga ~ wzrost, data = ais)
summary(ais_reg)

# Tak, istnieje statystycznie istotny związek
# waga = -126 + 1.11 * wzrost
# Waga wyjaśnia około 61% wariancji wzrostu

# wizualizacja regresji
ggplot(data = ais, aes(x = wzrost,y = waga))+
  geom_point()+
  geom_smooth(method = lm)

# Zadanie 6. Podziel dane na zbiór treningowy i testowy. Jaka jest wartość R-kwadrat i RMSE modelu przetestowanego na zbiorze testowym?

# Podział danych na zbiór uczący i testowy oraz walidacja modelu
set.seed(1234)
ais_split <- initial_split(ais)
ais_train <- training(ais_split)
ais_test <- testing(ais_split)

dim(ais_train)
dim(ais_test)

# Określenie rodzaju modelu
lm_spec <- linear_reg()

# Dopasowanie modelu do danych
lm_fit <- lm_spec %>%
  fit(wzrost ~ waga, data = ais)

ais_pred <- lm_fit %>% 
  predict(new_data = ais_test) %>% 
  bind_cols(ais_test)

# Obliczanie wartości R-kwadrat
rsq(data = ais_pred, truth = wzrost, estimate = .pred)

# Obliczanie rmse
rmse(data = ais_pred, truth = wzrost, estimate = .pred)
