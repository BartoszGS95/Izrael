numbers = []

number = int(input("podaj liczbe: "))
numbers.append(number)

number = int(input("podaj liczbe: "))
numbers.append(number)

number = int(input("podaj liczbe: "))
numbers.append(number)

number = int(input("podaj liczbe: "))
numbers.append(number)

number = int(input("podaj liczbe: "))
numbers.append(number)

print("suma liczb", sum(numbers))

print("najwieksza liczba", max(numbers))

print("najmniejsza liczba", min(numbers))

print("srednia arytmetyczna", sum(numbers)/len(numbers))

licznik_parzystych = 0
for number in numbers:
    if number % 2 == 0:
        print((number), "liczba jest parzysta")
        licznik_parzystych += 1
    else:
        print((number), "liczba jest nie parzysta")
print(licznik_parzystych, "ilosc liczb parzystych")

powtorzone = []

for number in numbers:

    if numbers.count(number) > 1 and number not in powtorzone:
        powtorzone.append(number)

print((powtorzone), "te liczba sie powtarza")

for number in powtorzone:

    while number in numbers:

        numbers.remove(number)
print((numbers), "te liczby zostaly")


kwadraty = []

for number in numbers:
    
    kwadraty.append(number**2) 
print((kwadraty), "to sa kwadraty liczb")