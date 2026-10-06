from turtle import *


def kwadrat(a):
    fillcolor("yellow")
    begin_fill()
    for _ in range(4):
        fd(a)
        lt(90)
    end_fill()


def poziom(ile):
    for i in range(ile):
        kwadrat(40)
        fd(40)

if __name__ == "__main__":
    poziom(3)
