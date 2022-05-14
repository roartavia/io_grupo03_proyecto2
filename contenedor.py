import itertools
import sys
import os.path
import time
from helper import BASH_COLORS, printHelp

class Articule:
    def __init__(self, key, weight, value):
        self.key = key
        self.weight = weight
        self.value = value

    def show(self):
        return f'{self.key + 1}, '

def main():

    if len(sys.argv) <= 1:
        printHelp('contenedor')
        return
    if sys.argv[1] == '-h':
        printHelp('contenedor')
        return
    if len(sys.argv) <= 2:
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

    startTime = time.time()
    if mode == '1':        
        runBruteForce(matrix)
    else:
        runDynamic(matrix)
    print(
        f'{BASH_COLORS.FAIL}Tiempo de ejecución: {"{:.8f}".format(time.time() - startTime)} segundos.{BASH_COLORS.ENDC}\n')

def printAnswer(h, bagStr):
    print (f'\nBeneficio máximo: {BASH_COLORS.OKGREEN}{h}{BASH_COLORS.ENDC}.')
    print (f'Incluidos: {BASH_COLORS.OKGREEN}{bagStr}{BASH_COLORS.ENDC}\n')
    
def runBruteForce(lines):
    print('Run brute force')

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
            newHeight = carryHeight + item.weight
            if newHeight <= bagWeight:
                carryHeight = newHeight
                carryValue = carryValue + item.value
            else:
                break
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
            maxH = newHeight
        else:
            break
    printAnswer(h=maxValue,bagStr=filledBag)

# Run the project
main() 

 