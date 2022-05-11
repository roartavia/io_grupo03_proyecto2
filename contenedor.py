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

import itertools
import sys
import os.path
import time
# local helper
from helper import BASH_COLORS, printHelp

class Articule:
    def __init__(self, key, weight, value):
        self.key = key
        self.weight = weight
        self.value = value

    def show(self):
        # TODO: change to only have the index 
        return f'({self.weight},{self.value}) '

def main():

    if len(sys.argv) <= 1:
        printHelp('contenedor')
        return
    if sys.argv[1] == '-h':
        printHelp('contenedor')
        return
    if len(sys.argv) <= 2:
        # user needs the [algoritm] and [fileinput]
        printHelp('contenedor')
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
        runBruteForce(matrix)
    else:
        runDynamic(matrix)
    print(
        f'{BASH_COLORS.FAIL}Tiempo de ejecución: {"{:.8f}".format(time.time() - startTime)} segundos.{BASH_COLORS.ENDC}\n')

def printAnswer(h, bagStr):
    # Output:
    # Beneficio máximo: 162
    # Incluidos: 3,4,5
    print (f'\nBeneficio máximo: {BASH_COLORS.OKGREEN}{h}{BASH_COLORS.ENDC}.')
    print (f'Incluidos: {BASH_COLORS.OKGREEN}{bagStr}{BASH_COLORS.ENDC}\n')
    
def runBruteForce(lines):
    print('Run brute force')
    # To have a better control of what index use an obj so you store the index for when the answer is needed
    # do all permutations, then check the valid permutations, and add the max value from that permutation 
    # the max value is when the carry weight is >= container weight or if you are at the end of the list
    # lines[0] - has the max weight
    # lines[1:] - has the rest of the value pairs, make them objs so you can do the permutations
    bagWeight = lines[0][0]
    articules = []
    for key, item in enumerate(lines[1:]):
        articules.append(Articule(key, weight=item[0], value=item[1]))

    permutations = (list(itertools.permutations(articules)))    
    maxValues = []

    for per in permutations:
        carryHeight = 0
        carryValue = 0
        for item in per:
            # but you also need to remove the rest of the items if you are not in the last item of the per
            newHeight = carryHeight + item.weight
            if newHeight <= bagWeight:
                carryHeight = newHeight
                carryValue = carryValue + item.value
            else:
                break
            #  make the sum if is valid add it if not then break
        # add the current weight for this per
        maxValues.append(carryValue)

    maxValue = max(maxValues)
    idx = maxValues.index(maxValue)
    maxH = 0
    filledBag = ''

    for item in permutations[idx]:
        newHeight = maxH + item.weight
        if newHeight <= bagWeight:
            # Context answ
            filledBag += articules[item.key].show()
            # PDF answer
            # filledBag += str(item.key + 1) + ", "
            maxH = newHeight
        else:
            break
    printAnswer(h=maxValue,bagStr=filledBag)

def runDynamic(lines):
    print('Run dynamic programming algoritm')
    # Pseudo code
    # V = [[0 for i in range(bagWeight)] for j in range(len(articules))]

    # for k in range(0, len(articules)):
    #     for w in range(bagWeight):
    #         if articules[k].weight > w:
    #             V[k][w] = V[k - 1][w]
    #         else:
    #             if articules[k].value + V[k - 1][w - articules[k].weight] > V[k - 1][w]:
    #                 V[k][w] = articules[k].value + V[k - 1][w - articules[k].weight]
    #             else:
    #                 V[k][w] = V[k - 1][w]
    # lines[0] - has the max weight
    # lines[1:] - has the rest of the value pairs, make them objs so you can do the permutations
    bagWeight = lines[0][0]
    articules = []
    for key, item in enumerate(lines[1:]):
        articules.append(Articule(key, weight=item[0], value=item[1]))

    dpMatrix = [[[0,[]] for i in range(bagWeight + 1)] for j in range(len(articules) + 1)]
 
    for i in range(len(articules) + 1):
        for w in range(bagWeight + 1):
            if i != 0 and w != 0:
                if articules[i-1].weight <= w and i != 0 and w != 0:
                    (dpMatrix[i][w])[0] = max(articules[i - 1].value + (dpMatrix[i - 1][w - articules[i - 1].weight])[0], (dpMatrix[i - 1][w])[0])
                    currentValue = articules[i - 1].value + (dpMatrix[i - 1][w - articules[i - 1].weight])[0]
                    if currentValue > (dpMatrix[i - 1][w])[0]:
                        # Add the new art to the bag
                        (dpMatrix[i][w])[1] = (dpMatrix[i - 1][w - articules[i - 1].weight])[1] + [articules[i - 1]]
                        (dpMatrix[i][w])[0] = currentValue
                    else:
                        (dpMatrix[i][w])[1] = (dpMatrix[i - 1][w])[1]
                        (dpMatrix[i][w])[0] = currentValue
                else:
                    (dpMatrix[i][w])[0] = (dpMatrix[i - 1][w])[0]
                    # Move the route
                    (dpMatrix[i][w])[1] = (dpMatrix[i - 1][w])[1]
    
    maxValue = dpMatrix[len(articules)][bagWeight][0]
    col = dpMatrix[len(articules)][bagWeight][1]
    ans = col[0].show()
    for i in range(1, len(col)):
        a = col[i]
        ans = f'{ans}{a.show()}'
    printAnswer(h=maxValue,bagStr=ans)
# Run the project
main() 

 