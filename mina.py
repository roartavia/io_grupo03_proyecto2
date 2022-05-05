#!/usr/bin/env python

# Una mina de oro de dimensiones n*m. Cada campo de la mina contienen un número entero positivo el cual es la cantidad de oro en toneladas.
# Inicialmente un minero puede estar en la primera columna pero en cualquier fila y puede mover a la derecha, diagonal arriba a la derecha
# o diagonal abajo a la derecha de una celda dada. El programa debe retornar la máxima cantidad de oro que el minero puede recolectar
# llegando hasta el límite derecho de la mina, y las casillas (camino) seleccionadas.
# Se deben programar dos versiones del algoritmos, el primero es fuerza bruta.

import itertools
import sys
import os.path
import time
# local helper
from helper import BASH_COLORS, printHelp

def main():

    if len(sys.argv) <= 1:
        printHelp('mina')
        return
    if sys.argv[1] == '-h':
        printHelp('mina')
        return
    if len(sys.argv) <= 2:
        # user needs the [algoritm] and [fileinput]
        printHelp('mina')
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

def printAnswer(value, routesStr):
    # Output : 16
    # Ejemplo de selección de casillas:
    # (2,0) -> (1,1) -> (1,2) -> (0,3) OR
    # (2,0) -> (3,1) -> (2,2) -> (2,3)
    print (f'\nOutput : {value}')
    print (f'Ejemplo de selección de casillas: \n{routesStr}\n')

def runBruteForce(lines):
    print('Run brute force')
    # Basically is a multiplications of arrays, each needed correspond to 
    # each column, that gives all the possible permutations
    # then sum each array result and get the ones with the max possible sum

    # The way you need to give the answer you need a tuple yo give the row you choose, 
    # use an obj same as the contenedor(?) (value, row)
    numCols = len(lines[0]) 
    cols = [[] for i in range(numCols)]
    for idxRow, row in enumerate(lines):
        for i in range(numCols):
            cols[i].append((row[i], idxRow))

    permutations = list(itertools.product(*cols))
    # have a list of indexes that have the indexes of the permutations that have the maxValue
    # have the maxValue stored
    maxGold = 0
    maxIndexes = []
    for i, per in enumerate(permutations):
        stepsTotal = 0
        for step in per: 
            stepsTotal+=step[0]
        # if sum of this per is greater clean the list and chagne the maxGold
        # if the sum is equal then add this to max indexes
        # else ignore
        if stepsTotal > maxGold:
            maxGold = stepsTotal
            maxIndexes = []
            maxIndexes.append(i)
        elif stepsTotal == maxGold:
            maxIndexes.append(i)
    finalRoutes = str(permutations[maxIndexes[0]]).replace("),", ") ->")
    for i in range(1,len(maxIndexes)):
        finalRoutes += f' OR \n{str(permutations[maxIndexes[i]]).replace("),", ") ->")}'

    printAnswer(maxGold, finalRoutes)


def runDynamic(lines):
    print('Run dynamic programming algoritm')

# Run the project
main() 

 