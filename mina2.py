#!/usr/bin/env python
from distutils.command.build_scripts import first_line_re
from operator import truediv
from unittest import result
from helper import BASH_COLORS, printHelp
import itertools
import sys
import os.path
import time


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
        Brute(matrix)
    else:
        Dynamic(matrix)
    print(
        f'{BASH_COLORS.FAIL}Tiempo de ejecución: {"{:.8f}".format(time.time() - startTime)} segundos.{BASH_COLORS.ENDC}\n')
def Dynamic(matrix):
    rows = len(matrix)
    columns = len(matrix[0])
    result=baseDimn(matrix,rows, columns)
    printAnswer(result[0],result[1])
# the recursion is started where the best candidate of each column is searched step by step
def baseDimn(matrix, rows, columns):
    col=columns-1
    aux=0
    solutioninit=auxDinm(matrix,aux,col,[])
    
    auxroute=[]
    while(aux<rows):
        solutionAux=auxDinm(matrix,aux+1,col,[])
        if(solutionAux[0]>solutioninit[0]):
            solutioninit=solutionAux
        for e in solutionAux[2]:
            auxroute.append(e)
        auxroute.append(solutionAux)
        aux+=1
        if(aux==rows):
            col-=1
            aux=0
        if (col < 0):
            break
    for route in auxroute:
        if(route[0]==solutioninit[0] and route[1]!=solutioninit[1] ):
            solutioninit[1]+= (" OR \n"+route[1])
    return solutioninit
#It parses the requested inputs that are right up, right down, and right
def auxDinm(matrix,i,j,list):
    if j==len(matrix[0]) or i<0 or i>len(matrix)-1:
        return [0,"",list]
    
    adelante=auxDinm(matrix,i,j+1,list)
    adelanteUp=auxDinm(matrix,i+1,j+1,list)
    adelanteDw=auxDinm(matrix,i-1,j+1,list)
    lista=[adelante,adelanteDw,adelanteUp]
    best=0
    rute=""
    
    for option in lista:
        if option[0]>best:
            best=option[0]
            rute=option[1]
        else:
            list.append([option[0]+matrix[i][j],f' -> ( {i} , {j} ) '+option[1]])
    return([matrix[i][j]+best,f' -> ( {i} , {j} )'+rute,list])
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

def Brute(matrix):
    mAux=[]
    mAux=getTransposeMatrix(matrix)
    permutations = list(itertools.product(*mAux))
    oroMax=0
    auxpasos=[]
    rufin=''
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
        if(stepsTotal>=oroMax and isValid):
            oroMax=stepsTotal
            auxpasos.append([oroMax,per])
    first=True
    for rut in auxpasos:
        sRut=''
        if(rut[0]==oroMax):
            if (first==True):
                first=False
            else:
                sRut+=' OR \n'
            aux=True
            for cont,step in enumerate(rut[1]):
                sRut+= f'( {step[1]} , {cont} )'
                if(cont==len(rut[1])-1):
                    aux=False
                if (aux):
                    sRut+=' - > '
            rufin+=sRut
    printAnswer(oroMax,rufin)







    return True
main()