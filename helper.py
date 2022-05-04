#!/usr/bin/env python

class BASH_COLORS:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def printHelp(name):
    print('\n')
    print(f'{BASH_COLORS.WARNING}Para ejecutar el programa, debe pasar el archivo con el formato de entrada correcto como parámetro y el algoritmo a usar, 1 para brute force o 2 para DP{BASH_COLORS.ENDC}.')
    print('Ejemplo:')
    print('\n')
    print(f'{BASH_COLORS.OKGREEN}python {name}.py [algoritmo: 1 or 2] filename.txt{BASH_COLORS.ENDC}')
    print('\n')
