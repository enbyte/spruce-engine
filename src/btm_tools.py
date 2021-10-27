import os
import copy
import logging
import csv
import numpy
from pprint import pprint

logging.basicConfig(format='%(levelname)s at %(asctime)s (file %(filename)s :: %(lineno)d): %(message)s')

def convert_mat(mat, dtype):
    '''
    Convert a matrix to a given datatype
    '''
    return numpy.array(mat).astype(dtype).tolist()
    

###################
# Matrix Tools    #
###################




def matrix(what, height, length):
    '''
    Create a matrix, height by length, and return it.
    '''
    row_build = []
    build = []
    for x in range(length):
        row_build.append(what)
    for i in range(height):
        build.append(copy.deepcopy(row_build))
    return build

def get_row(mat, row):
    '''
    Get a given row of a matrix
    '''
    return mat[row]


def get_col(mat,col):
    '''
    Get a given column of a matrix.
    '''
    v = [x[col] for x in mat]
    return v


def subsection(matrix, firstrow, lastrow, firstcolumn, lastcolumn, includeLast=True):
    if not includeLast:
        inc = 0
    else:
        inc = 1
    t = [x[firstrow:lastrow+inc] for x in matrix[firstcolumn:lastcolumn+inc]]
    return t

def longest_item_in_list(list_):
    top = list_[0] - 1
    for item in list_:
        if len(item) > top:
            top = len(item)
    return top

def matToList(mat):
    b = []
    for row in mat:
        b.extend(row)
    return b


######################
# File Tools
######################




class MatrixMissingAttributeError(Exception): pass


def load_mat(file, delimiter=',', dtype=int):
    '''
    Load a matrix from a given file.
    '''
    if file == '':
        logging.error('File cannot be a null string')
        raise NameError
    with open(file) as f:
        reader = csv.reader(f, delimiter=delimiter)
        x = list(reader)
        return convert_mat(x, dtype)

def save(matrix, filename, clearfile=True):
    if filename == '':
        logging.error('Filename cannot be null')
        raise NameError
    if clearfile:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass
    with open(filename, 'a+') as f:
        for row in matrix:
            rowcp = []
            for i in row:
                rowcp.append(str(i))
            f.write(','.join(rowcp) + '\n')
                

if __name__ == '__main__': #self-test code
    mat = matrix(0, 10, 10)
    save(mat, 'tools_py_TEST')
    if True:
        m = load_mat('tools_py_TEST')
        match  = (m == mat)
        if not match:
            print("Failed!\nM1:")
            pprint(m)
            print("M2:")
            pprint(mat)
        else:
            print("Test complete, passed")
        



              
