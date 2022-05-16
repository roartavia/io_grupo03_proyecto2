#!/usr/bin/env python
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
        Dynamic(matrix)
    else:
        Dynamic(matrix)
    print(
        f'{BASH_COLORS.FAIL}Tiempo de ejecución: {"{:.8f}".format(time.time() - startTime)} segundos.{BASH_COLORS.ENDC}\n')
def Dynamic(matrix):
      #Largo rows
    rows = len(matrix)
    #Largo columns
    columns = len(matrix[0])
    result=baseDimn(matrix,rows, columns)
    printAnswer(result[0],result[1])
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
main()