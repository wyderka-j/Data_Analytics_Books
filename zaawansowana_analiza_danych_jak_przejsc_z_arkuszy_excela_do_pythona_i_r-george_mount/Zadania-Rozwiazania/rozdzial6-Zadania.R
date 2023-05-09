#Zadanie 1. W menu wybierz Tools/Global Options/Appearance i dostosuj czcionkę i motyw edytora.

# 1. Preferuję motyw Pastel On Dark

#Zadanie 2. W RStudio utwórz skrypt, który wykona następujące czynności:

# Przypisze sumę 1 i 4 do obiektu a
a <- sum(1,4)

# Przypisze pierwiastek kwadratowy z a bo b
b <- sqrt(a)

# Przypisze b minus 1 do obiektu d.
d <- b - 1

#  Jakiego typu dane są przechowywane w d?
str(d)

#  Czy d jest większe niż 2?
d > 2

# Zadanie 3. Zainstaluj pakiet psych z repozytorium CRAN i załaduj go do swojej sesji. 
# W komentarzach wyjaśnij różnicę między instalacją a wczytaniem pakietu.

# Instalacja to jednorazowa czynność polegająca na pobraniu pakietu z repozytorium CRAN
# install.packages('psych')

# i załaduj go do swojej sesji. 
# Ładowanie musi być wykonane w każdej sesji, w której chcemy skorzystać z pakietu
library(psych)