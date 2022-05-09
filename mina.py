#!/usr/bin/env python

# Una mina de oro de dimensiones n*m. Cada campo de la mina contienen un número entero positivo el cual es la cantidad de oro en toneladas.
# Inicialmente un minero puede estar en la primera columna pero en cualquier fila y puede mover a la derecha, diagonal arriba a la derecha
# o diagonal abajo a la derecha de una celda dada. El programa debe retornar la máxima cantidad de oro que el minero puede recolectar
# llegando hasta el límite derecho de la mina, y las casillas (camino) seleccionadas.
# Se deben programar dos versiones del algoritmos, el primero es fuerza bruta.

import itertools
from select import select
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

def getTransposeMatrix(matrix, isEmpty = False):
    numCols = len(matrix[0]) 
    cols = [[] for i in range(numCols)]
    for idxRow, row in enumerate(matrix):
        for i in range(numCols):
            if isEmpty:
                cols[i].append((0, idxRow))
            else: 
                cols[i].append((row[i], idxRow))
    return cols

# TODO: Fix the brute force to gice the # of the row instead of the value so it matches the final ans of the 
# DP problem
def runBruteForce(lines):
    print('Run brute force')
    # Basically is a multiplications of arrays, each needed correspond to 
    # each column, that gives all the possible permutations
    # then sum each array result and get the ones with the max possible sum

    # The way you need to give the answer you need a tuple yo give the row you choose, 
    # use an obj same as the contenedor(?) (value, row)
    cols = getTransposeMatrix(lines)
    permutations = list(itertools.product(*cols))
    # have a list of indexes that have the indexes of the permutations that have the maxValue
    # have the maxValue stored
    maxGold = 0
    maxIndexes = []
    for i, per in enumerate(permutations):
        isValid = True
        stepsTotal = 0
        # You need to check first if you can go from this index to the next step
        for j,step in enumerate(per):
            # if index is -1 or +1 of prev then is a valid move 
            if j != 0:
                if step[1] - 1 == per[j - 1][1] or step[1] + 1 == per[j - 1][1] or step[1] == per[j - 1][1]:
                    stepsTotal += step[0]
                else:
                    isValid = False
                    break
            else:
                stepsTotal += step[0]
        # if sum of this per is greater clean the list and chagne the maxGold
        # if the sum is equal then add this to max indexes
        # else ignore
        if isValid:
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
    # Do the cols for rows, then for each new row get the max possible add this max to the matrix of ans
    # do the same for the n new rows, then you can the route
    # just need to resolve each n-1 -> n relationship, get the max item in the col n, 
    # n-1 can go to top right, right or down right (top right or down right maybe don't exist because n-1 can be 
    # placed in the top border or in the bottom border)
    lenCols = len(lines[0])
    lenRows = len(lines)
    # create the matrix to store the possible routes and the carry gold
    # [0] - has the gold
    # [0] - the route to achieve this amount
    posibleMaxValues = [[[0,[]] for i in range(lenCols)] for j in range(lenRows)]
    
    # iterate from bottom to top, ignore the first col because it doesn't have other col behind
    for col in range(lenCols - 1, -1, -1):
        for row in range(lenRows):
            right = (0,0)
            topRight = (0,0)
            downRight = (0,0)

            rightIndex = col + 1
            if col != (lenCols - 1):
                right = (posibleMaxValues[row][rightIndex][0], row)
            # if you are in the border top
            if row != 0 and col != lenCols - 1:
                topRight = (posibleMaxValues[row - 1][rightIndex][0], row - 1)
            # if you are in the border bottom
            if row != lenRows - 1 and col != lenCols - 1:
                downRight = (posibleMaxValues[row + 1][rightIndex][0], row + 1)
  
            # Max from right vals
            posibleSteps = [right, topRight, downRight]
            maxRight = max(posibleSteps, key=maxValue)

            posibleMaxValues[row][col][0] = lines[row][col] + maxRight[0]
            # we are doing this wrong, you need to copy all the route of the max position, and not 
            # build in the col 0, you need for the current col copy the n better rroute in col prev, not only the 
            # prev pos - is all the route
            if right == (0,0):
                # add the route 
                posibleMaxValues[row][col][1] = [[row]]
            else: 
                # Now that you have the carry result, start adding the routes to get there
                setpsWithMax = list(filter(lambda step: step[0] == maxRight[0], posibleSteps))
                # this have the better index in 
                # septs[1] so for each step get the index and this is going to be 
                newRoutes = []
                # [col] product the prev selected?
                newStep = [row]
                for step in setpsWithMax:
                    prevRoutes = posibleMaxValues[step[1]][col+1][1]
                    for prevRoute in prevRoutes:
                        t = newStep + prevRoute
                        newRoutes.append(t)
                
                posibleMaxValues[row][col][1] = newRoutes
                # select the best possible rows

    # then for each row you can add the i in the possible values     
    # The max possible value is in one of the rows in the 1st column
    bestIndexes = [0]
    for i in range(1, lenRows):
        if posibleMaxValues[i][0][0] > posibleMaxValues[bestIndexes[0]][0][0]:
            bestIndexes = [i]
        elif posibleMaxValues[i][0][0] == posibleMaxValues[bestIndexes[0]][0][0]:
            bestIndexes.append(i)
    finalRoutes = ''

    for i in bestIndexes:
        for route in posibleMaxValues[i][0][1]:
            strRoute = f'({route[0]}, 0)'
            
            for stepIdx in range(1,len(route)):
                strRoute += f' -> ({route[stepIdx]}, {stepIdx})' 

            if finalRoutes == '':
                finalRoutes = strRoute
            else: 
                finalRoutes = f'{finalRoutes} OR \n{strRoute}' 
    printAnswer(posibleMaxValues[bestIndexes[0]][0][0], finalRoutes)

def maxValue(tuple):
    return tuple[0]

# Run the project
main()

 