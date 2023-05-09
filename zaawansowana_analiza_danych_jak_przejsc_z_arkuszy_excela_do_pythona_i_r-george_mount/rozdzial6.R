#proste operacje matematyczne
1 * 2
3 + 5 - 4

1:50

#operator ?
?sqrt

# Przyklad funkcii sqrt dostepny wc opisie funkcji
require(stats) # for spline
require(graphics)
xx <- -9:9
plot(xx, sqrt(abs(xx)),  col = "red")
lines(spline(xx, sqrt(abs(xx)), n=101), col = "pink")


# Mnożenie przed dodawaniem
3 * 5 + 6 

# Dzielenie przed odejmowaniem
2 / 2 - 7

1 * 2 # To dopuszczalny sposób komentowania kodu

# Ten sposób jest preferowany
2 * 1

# Ile wynosi wartość bezwzględna z -100?
abs(-100)

# To nie zadziała!
ABS(-100)
Abs(-100)

# Konwersja na duże litery
toupper('Kocham R')

# Czy 3 jest większe od 4?
3 > 4

# Przypisywanie wartości do obiektu w R
my_first_object = abs(-100)

# Wyświetlanie obiektu w R
my_first_object

my_second_object <- sqrt(abs(-5 ^ 2))
my_second_object


#najpopularniejsze typy danych
my_char <- 'Witaj, świecie' 
my_other_char <- "Możemy programować w R!" 
my_num <- 3
my_other_num <- 3.21
my_int <- 12L 
my_logical <- FALSE
my_other_logical <- F

#funkcja str()- sprawdzenie struktury obiektu
str(my_char)
str(my_num)
str(my_int)
str(my_logical)

# Czy my_num jest równe 5.5?
my_num == 5.5

# Liczba znaków w obiekcie my_char
nchar(my_char)

#ponowne przypisanie wartosci
my_other_num <- 2.2
my_num <- my_num/my_other_num
my_num

# Dołączenie tidyverse do bieżącej sesji
library(tidyverse)
