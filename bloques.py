# Se tienen una cantidad bloques de madera tridimensionales, cada uno con medida de Largo (L), Ancho (W) y Altura (H).
# Se deben poner uno encima de otro de manera que se logre hacer la torre más alta posible. Sin embargo un bloque
# puede ir encima del otro si su base es estrictamente menor que superficie superior del bloque de abajo.
# Esto quiere decir que las dimensiones de Largo y Ancho (base) son estrictamente menores al bloque inferior.
# Los bloques se pueden rotar en sus dimensiones, y se pueden usar más de un bloque según las rotaciones del mismo tipo
# para formar la torre. Cada bloque tiene 3 posibles rotaciones.

# Debe implementar la solución con fuerza bruta y programación dinámica.

#!/usr/bin/env python
import sys
import os.path


class BASH_COLORS:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def main():

    if len(sys.argv) <= 1:
        # display help (?)
        return
    if sys.argv[1] == "-h":
        # display help (?)
        return
    if len(sys.argv) < 2:
        # user needs the [algoritm] and [fileinput]
        # display help (?)
        return

    mode = sys.argv[1]
    fileName = sys.argv[2]

    if not os.path.isfile(fileName):
        print("File does not exist.")
        return

    f = open(fileName, "r")
    lines = f.readlines()
    matrix = []
    for line in lines:
        row = line.strip().split(",")
        matrix.append(row)

    if mode == "1":
        # brute force
        runBruteForce(matrix)
    else:
        runDynamic(matrix)


def runBruteForce(lines):
    print(lines)
    print("Run the brute force algoritm")


def runDynamic(lines):
    print(lines)
    print("Run dynamic programming algoritm")


# Run the project
main()
