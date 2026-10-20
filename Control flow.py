def zad1():
    liczby = []

    for i in range(-1, 1001):
        liczby.append(i)

    return liczby


def czy_pierwsza(liczba):
    if liczba < 2:
        return False

    for dzielnik in range(2, liczba):
        if liczba % dzielnik == 0:
            return False

    return True


def zad2(liczby):
    pierwsze = []

    for liczba in liczby:
        if czy_pierwsza(liczba):
            pierwsze.append(liczba)

    return pierwsze


def zad3(liczby):
    ile = 0

    for liczba in liczby:
        if czy_pierwsza(liczba):
            ile = ile + 1

    return ile

# import math
#
# r = float(input("Podaj promień kuli: "))
# V = (4 / 3) * math.pi * r**3
# print("Objętość kuli wynosi:", V)

# n = int(input("Ile razy napisać 'Kocham programować'? "))
#
# for i in range(n):
#     print("Kocham programować")

# suma = 0
#
# while True:
#     liczba = input("Podaj liczbę do sumy lub wpisz stop: ")
#
#     if liczba == "stop":
#         break
#
#     suma = suma + int(liczba)
#
# print("Suma liczb:", suma)

# suma = 0
# licznik = 0
#
# while True:
#     liczba = input("Podaj liczbę do średniej lub wpisz stop: ")
#
#     if liczba == "stop":
#         break
#
#     suma = suma + float(liczba)
#     licznik = licznik + 1
#
# if licznik > 0:
#     srednia = suma / licznik
#     print("Średnia arytmetyczna:", srednia)
# else:
#     print("Nie podano żadnych liczb.")

n = int(input("Podaj n: "))
suma = 0

for i in range(n):
    suma = suma + 2**i

print("Suma potęg liczby 2:", suma)
