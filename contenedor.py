#!/usr/bin/env python

# Se tienen n elementos distintos, y un contenedor que soporta una cantidad especifica de peso W.
# Cada elemento i tiene un peso wi, un valor o beneficio asociado dado por bi.
# El problema consiste en agregar elementos al contenedor de forma que se maximice el beneficio
# total sin superar el peso máximo que soporta el contenedor. La solución debe ser dada con la
# lista de los elementos que se ingresaron y el valor del beneficio máximo obtenido.

# Se deben programar dos versiones del algoritmos, el primero es fuerza bruta,
# también llamada búsqueda exhaustiva, pero no se debe confundir con backtracking.
# El segundo es programación dinámica (implementación bottom-up visto en clase).
# El algoritmo a correr debe ser indicado como parámetros en la linea de entrada del programa.
# Con dos parámetros, el tipo de algoritmo a correr y el archivo con los datos del problema.

import sys
import os.path
import time


class BASH_COLORS:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def main():

    if len(sys.argv) <= 1:
        printHelp()
        return
    if sys.argv[1] == '-h':
        printHelp()
        return
    if len(sys.argv) <= 2:
        # user needs the [algoritm] and [fileinput]
        printHelp()
        return

    mode = sys.argv[1]
    fileName = sys.argv[2]

    if not os.path.isfile(fileName):
        print('File does not exist.')
        return

    f = open(fileName, 'r')
    lines = f.readlines()
    matrix = []
    for line in lines:
        row = [int(item) for item in line.strip().split(',')]
        matrix.append(row)
    # Start exc
    startTime = time.time()
    if mode == '1':
        # brute force
        runBruteForce(matrix)
    else:
        runDynamic(matrix)
    print(
        f'{BASH_COLORS.FAIL}Tiempo de ejecución: {"{:.8f}".format(time.time() - startTime)} segundos.{BASH_COLORS.ENDC}\n')

def printHelp():
    print('\n')
    print(f'{BASH_COLORS.WARNING}Para ejecutar el programa, debe pasar el archivo con el formato de entrada correcto como parámetro y el algoritmo a usar, 1 para brute force o 2 para DP{BASH_COLORS.ENDC}.')
    print('Ejemplo:')
    print('\n')
    print(f'{BASH_COLORS.OKGREEN}python contenedor.py [algoritmo: 1 or 2] filename.txt{BASH_COLORS.ENDC}')
    print('\n')

def printAnswer():
    print('Answer')
    
def runBruteForce(lines):
    print('Run brute force')    

def runDynamic(lines):
    print('Run dynamic programming algoritm')

# Run the project
main() 

 