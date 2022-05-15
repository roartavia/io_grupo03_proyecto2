import itertools
import sys
import os.path
import time
from helper import BASH_COLORS, printHelp

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


def printAnswer(profits,solution):
    for i in range(0, len(profits)):
        auxSum = profits[i]
        auxArray = []
        auxArray.append(i+1)
        for j in range(i + 1, len(profits)):
            auxSum = profits[j] + auxSum
            auxArray.append(j+1)
            if auxSum == solution:
                return auxArray


def containerBruteForce(bagWeight, weights, profits, len):
    #Base case
    if len == 0 or bagWeight == 0:
        return 0

    #if weight on n item is more than the bag
    #cannot be included
    if (weights[len - 1] > bagWeight):
        return containerBruteForce(bagWeight, weights, profits, len - 1)

    #return max of n item included
    else:
        return max(profits[len - 1] + containerBruteForce(bagWeight - weights[len - 1], weights, profits, len - 1),
                   containerBruteForce(bagWeight, weights, profits, len - 1))


def containerDynamicProgramming(bagWeight, weights, profits, len):
    dp = [0 for i in range(bagWeight + 1)]  # Making the array

    for i in range(1, len + 1):  # taking first i elements
        for j in range(bagWeight, 0, -1):  # starting from back,so that we also have data of
                                           # previous computation when taking i-1 items
            if weights[i - 1] <= j:
                # finding the maximum value
                dp[j] = max(dp[j], dp[j - weights[i - 1]] + profits[i - 1])

    return dp[bagWeight]  # returning the maximum value of knapsack

def runBruteForce(lines):
    print('Run brute force\n')

    # bagWeight always first line
    bagWeight = lines[0][0]
    weights = []
    profits = []

    # articules goes second line onwards
    for key, item in enumerate(lines[1:]):
        weights.append(item[0])
        profits.append(item[1])

    solution = containerBruteForce(bagWeight, weights, profits, len(profits))
    print("Output:")
    print("Beneficio máximo: ",solution)
    print("Inlcuidos: ",printAnswer(profits, solution))


def runDynamic(lines):
    print('Run dynamic programming algorithm\n')

    # bagWeight always first line
    bagWeight = lines[0][0]
    weights = []
    profits = []

    # articules goes second line onwards
    for key, item in enumerate(lines[1:]):
        weights.append(item[0])
        profits.append(item[1])

    solution = containerDynamicProgramming(bagWeight, weights, profits, len(profits))
    print("Output:")
    print("Beneficio máximo: ", solution)
    print("Inlcuidos: ", printAnswer(profits, solution))

main()
