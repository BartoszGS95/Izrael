import random


# Zadanie 1
def zad1():
    lista = list(range(-1, 1001))
    return lista


# Funkcja pomocnicza do sprawdzania liczb pierwszych
def czy_pierwsza(n):
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


# Zadanie 2
def zad2(lista):
    pierwsze = []

    for liczba in lista:
        if czy_pierwsza(liczba):
            pierwsze.append(liczba)

    return pierwsze


# Zadanie 3
def zad3(lista):
    ile = 0

    for liczba in lista:
        if czy_pierwsza(liczba):
            ile += 1

    return ile


# Zadanie 4 - NWD
def zad4(a, b):
    a = abs(a)
    b = abs(b)

    while b != 0:
        reszta = a % b
        a = b
        b = reszta

    return a


# Zadanie 5 - NWW
def zad5(a, b):
    if a == 0 or b == 0:
        return 0

    return abs(a * b) // zad4(a, b)


# Zadanie 6
def zad6(a):
    pierwsza = random.randint(0, a)
    druga = random.randint(0, a - pierwsza)
    trzecia = a - pierwsza - druga

    return [pierwsza, druga, trzecia]


# ----------------------------------------------
# Program do sprawdzania zadań
# Odkomentuj test, który chcesz wykonać
# ----------------------------------------------

# odp_zad_1, AAA = zad1(), zad1()
# odp_zad_2 = zad2(AAA)
# odp_zad_3 = zad3(AAA)
# odp_zad_4 = zad4(78, 66)
# odp_zad_5 = zad5(78, 66)
# odp_zad_6 = zad6(100)

plusy = 0

# if len(odp_zad_1) == 1002:
#     plusy += 1
#     print("odp_zad_1 Good Job!!!")

# if len(odp_zad_2) == 168:
#     plusy += 1
#     print("odp_zad_2 Good Job!!!")

# if odp_zad_3 == 168:
#     plusy += 1
#     print("odp_zad_3 Good Job!!!")

# if odp_zad_4 == 6:
#     plusy += 1
#     print("odp_zad_4 Good Job!!!")

# if odp_zad_5 == 858:
#     plusy += 1
#     print("odp_zad_5 Good Job!!!")

# if sum(odp_zad_6) == 100:
#     plusy += 1
#     print("odp_zad_6 Good Job!!!")

print("==" * 10)
print(f"Twoja obecna ocena {plusy}")
print("==" * 10)
