# Se tienen una cantidad bloques de madera tridimensionales, cada uno con medida de Largo (L), Ancho (W) y Altura (H).
# Se deben poner uno encima de otro de manera que se logre hacer la torre más alta posible. Sin embargo un bloque
# puede ir encima del otro si su base es estrictamente menor que superficie superior del bloque de abajo.
# Esto quiere decir que las dimensiones de Largo y Ancho (base) son estrictamente menores al bloque inferior.
# Los bloques se pueden rotar en sus dimensiones, y se pueden usar más de un bloque según las rotaciones del mismo tipo
# para formar la torre. Cada bloque tiene 3 posibles rotaciones.

# Debe implementar la solución con fuerza bruta y programación dinámica.

#!/usr/bin/env python
import itertools
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
        row = [int(item) for item in line.strip().split(",")]
        matrix.append(row)
    # Start exc
    start_time = time.time()
    if mode == "1":
        # brute force
        runBruteForceFixed(matrix)
    else:
        runDynamic(matrix)
    print(
        f'{BASH_COLORS.FAIL}Tiempo de ejecución: {"{:.8f}".format(time.time() - start_time)} segundos.{BASH_COLORS.ENDC}')

def printAnswer(height, stack):
    print(f'Output: altura máxima {BASH_COLORS.OKGREEN}{height}{BASH_COLORS.ENDC}.')
    print(f'Bloques: {BASH_COLORS.OKGREEN}{stack}.{BASH_COLORS.ENDC}')

def getRotations(block):
    # there are 3 posible diff heights for a block
    rotations = []
    # TODO: ignore the items that are already in the list
    rotations.append(block)
    rotations.append([block[0], block[2], block[1]])
    rotations.append([block[1], block[2], block[0]])
    return rotations


def getAllRotations(blocks):
    rotations = []
    for block in blocks:
        rotations.append(block)
        # don't use a rotation that is already in the array
        firstRotation = [max(block[0], block[2]),min(block[0], block[2]), block[1]]
        if not firstRotation in rotations:
            rotations.append(firstRotation)
        secondRotation = [max(block[1], block[2]),min(block[1], block[2]), block[0]]
        if not secondRotation in rotations:
            rotations.append(secondRotation)
 
    return rotations

def runBruteForce(lines):
    # the lines format are:
    # Largo (L), Ancho (W) y Altura (H)
    # [
    #     ['2', ' 3', ' 3'],
    #     ['2', ' 4', ' 6'],
    #     ['1', ' 1', ' 4']
    # ]
    posibles = getAllRotations(lines)
    # This doesnt reuse the blocks
    universe = list(itertools.product(*posibles))
    bestStack = []
    bestHeight = 0
    for galaxy in universe:
        posibleStacks = (list(itertools.permutations(galaxy)))
        for stack in posibleStacks:
            # start with the base height
            currentHeight = stack[0][2]
            currentStack = [stack[0]]
            for i in range(0, len(stack) - 1):
                # add the next block height, the current is already added
                # if h and w greater then isValid = false and break
                if (stack[i][0] <= stack[i+1][0] or stack[i][1] <= stack[i+1][1]) and (stack[i][0] <= stack[i+1][1] or stack[i][1] <= stack[i+1][0]):
                    # TODO: check if one extra rotations is needed for displaying purposes
                    break
                # else-  sum the height
                currentHeight += stack[i + 1][2]                
                currentStack.append(stack[i + 1])
            if currentHeight > bestHeight:
                bestHeight = currentHeight
                bestStack = currentStack
    print(
    f'The best posible stack is: {bestStack} with the height {bestHeight}.')
    # return [bestStack, bestHeight]

def runBruteForceFixed(lines):
    print ("Run the brute force algoritm")
    # the lines format are:
    # Largo (L), Ancho (W) y Altura (H)
    # [
    #     ['2', ' 3', ' 3'],
    #     ['2', ' 4', ' 6'],
    #     ['1', ' 1', ' 4']
    # ]
    blocks = getAllRotations(lines)

    # you don't need to do a multiplications, because you can reuse the block so have all the posible rotations in the same blocks list and 
    # do the permutations to the all list
    posibleStacks = (list(itertools.permutations(blocks)))
    bestStack = []
    bestHeight = 0
    for stack in posibleStacks:
        # start with the base height
        currentHeight = stack[0][2]
        currentStack = [stack[0]]
        for i in range(0, len(stack) - 1):
            # add the next block height, the current is already added
            # if h and w greater then isValid = false and break
            if (stack[i][0] <= stack[i+1][0] or stack[i][1] <= stack[i+1][1]) and (stack[i][0] <= stack[i+1][1] or stack[i][1] <= stack[i+1][0]):
                # TODO: check if one extra rotations is needed for displaying purposes
                break
            # else-  sum the height
            currentHeight += stack[i + 1][2]                
            currentStack.append(stack[i + 1])
        if currentHeight > bestHeight:
            bestHeight = currentHeight
            bestStack = currentStack
    printAnswer(height=bestHeight, stack=bestStack)
 

def maxArea(block):
    return block[0] * block[1]


def runDynamic(lines):
    print("Run dynamic programming algoritm")
    # the lines format are:
    # Largo (L), Ancho (W) y Altura (H)
    # [
    #     ['2', ' 3', ' 3'],
    #     ['2', ' 4', ' 6'],
    #     ['1', ' 1', ' 4']
    # ]
    permutations = getAllRotations(lines)
    blocks = sorted(permutations, key=maxArea, reverse=True)
    maxsHeights = []
    routes = []
    for i, block in enumerate(blocks):
        maxsHeights.append(block[2])
        routes.append(i)

    for i in range(1, len(blocks)):
        for j in range(0, i):
            # Do the extra rotation in the x axis
            if (blocks[i][0] < blocks[j][0] and blocks[i][1] < blocks[j][1]) \
                or (blocks[i][0] < blocks[j][1] and blocks[i][1] < blocks[j][0]):
                possibleNewHeight = maxsHeights[j] + blocks[i][2]
                if possibleNewHeight > maxsHeights[i]:
                    maxsHeights[i] = possibleNewHeight
                    routes[i] = j

    maxHeight = max(maxsHeights)
    swap = maxsHeights.index(maxHeight)
    finalStack = []
    while True:
        finalStack.insert(0,blocks[swap])
        current = routes[swap]
        if current == swap:
            break
        swap = current
    printAnswer(height=maxHeight, stack=finalStack)

# Run the project
main() 

 
 
