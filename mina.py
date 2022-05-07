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
            # TODO: missing when is hte same there are more than 1 possible max
            posibleSteps = [right, topRight, downRight]
            maxRight = max(posibleSteps, key=maxValue)

            setpsWithMax = list(filter(lambda step: step[0] == maxRight[0], posibleSteps))
            # print ("====")
            # print (setpsWithMax)
            # print ("====")

            # iterate for the 3 items to search the if is unique or n
            posibleMaxValues[row][col][0] = lines[row][col] + maxRight[0]
            # if there are more than 1 then a new three is made, copy the current list the n times and for each
            # item in maxes insert the max in the bifurcacion
            # if there isn't lists in posibleMaxValues[row][0])[1]
            if right != (0,0):
                savedRoutesForRow = (posibleMaxValues[row][0])[1]
                if len(savedRoutesForRow) == 0:
                    # then create as new one for each steps with max 
                    for newStep in setpsWithMax:
                        # insert a new list with the step
                        # print (newStep)
                        savedRoutesForRow.append([newStep])
                    # (posibleMaxValues[row][0])[1].insert(0,(lines[maxRight[1]][col], maxRight[1]))
                    (posibleMaxValues[row][0])[1] = savedRoutesForRow
                    print (savedRoutesForRow)
                    print ('++++++++++++')
                else:
                    # [[(15, 1)], [(15, 0)]]]
                    currentRoutes = savedRoutesForRow.copy()
                    print ("====")
                    print (currentRoutes)
                    print (setpsWithMax)
                    print ("====")
                    newTotal = []
                    # # if there are already lists in there, for each list append each steps with max
                    for current in currentRoutes:
                        for newStep in setpsWithMax:
                            temp = current.copy()
                            # print (temp)
                            # print (lines[newStep[1]][col])
                            temp.insert(0,(lines[newStep[1]][col], newStep[1]))
                            newTotal.append(temp)
                    (posibleMaxValues[row][0])[1] = newTotal
                    # for newStep in posibleSteps:
                    # print (newTotal)
                    # (posibleMaxValues[row][0])[1].insert(0,(lines[maxRight[1]][col], maxRight[1]))
            
    # print (posibleMaxValues)                                 
    # The max possible value is in one of the rows in the 1st column
    # res = posibleMaxValues[0][0][0]
    bestIndexes = [0]
    for i in range(1, lenRows):
        # print (posibleMaxValues[i][0])
        if posibleMaxValues[i][0][0] > posibleMaxValues[bestIndexes[0]][0][0]:
            bestIndexes = [i]
        elif posibleMaxValues[i][0][0] == posibleMaxValues[bestIndexes[0]][0][0]:
            bestIndexes.append(i)
    print ("===")
    print (bestIndexes)
    for i in range(lenRows):
        print (posibleMaxValues[i][0])
    
    # print (ans)

def maxValue(tuple):
    return tuple[0]


# Run the project
main()

 