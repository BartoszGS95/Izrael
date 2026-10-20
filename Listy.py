import random


# def zad4(a, b):
#     a = abs(a)
#     b = abs(b)
#
#     while b != 0:
#         reszta = a % b
#         a = b
#         b = reszta
#
#     return a


# def zad5(a, b):
#     if a == 0 or b == 0:
#         return 0
#
#     return abs(a * b) // zad4(a, b)


def zad6(a):
    pierwsza = random.randint(0, a)
    druga = random.randint(0, a - pierwsza)
    trzecia = a - pierwsza - druga

    return [pierwsza, druga, trzecia]


n = int(input("Ile elementów wylosować? "))
minimum = int(input("Podaj minimum: "))
maksimum = int(input("Podaj maksimum: "))

lista = []

for i in range(n):
    liczba = random.randint(minimum, maksimum)
    lista.append(liczba)

print(lista)

lista = [1, 1, 1, 5, 5, -2, 10, 1]

minimum = lista[0]
maksimum = lista[0]

for liczba in lista:
    if liczba < minimum:
        minimum = liczba

    if liczba > maksimum:
        maksimum = liczba

print("Minimum:", minimum)
print("Maksimum:", maksimum)

lista = [2, 5, 2, 7, 2, 9, 5]
n = int(input("Jaką liczbę policzyć? "))

ile = 0

for liczba in lista:
    if liczba == n:
        ile += 1

print("Liczba występuje", ile, "razy")

lista = [6, 10, 12, 15, 20, 7, 9, 30]
n = int(input("Podaj dzielnik n: "))

ile = 0

for liczba in lista:
    if liczba % n == 0:
        ile += 1

print("Liczb podzielnych przez", n, "jest:", ile)

lista = [3, 8, 1, 6, 2, 9, 4]
n = int(input("Podaj n: "))

druga_lista = []

for liczba in lista:
    if liczba < n:
        druga_lista.append(liczba)

print(druga_lista)

n = int(input("Ile liczb podasz? "))

parzyste = []

for i in range(n):
    liczba = int(input("Podaj liczbę: "))

    if liczba % 2 == 0:
        parzyste.append(liczba)

print("Liczby parzyste:", parzyste)
print("Liczba parzystych:", len(parzyste))
