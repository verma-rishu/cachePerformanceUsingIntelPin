import random
import pdb
import argparse
import os
import math
import numpy as np
from scipy import sparse

parser = argparse.ArgumentParser(description='Input Matrix generator')
parser.add_argument('--seed', type=int, default=0, help='Seed Value')
parser.add_argument('--n', type=int, default=3, help='Matrix order(nxn)')
parser.add_argument('--sparsity', type=int, default=0, help='Sparisty of input data matrix in %')
#parser.add_argument('--indexSparsity', type=int, default=0, help='Sparisty of index matrix in %')
parser.add_argument('--dump', type=str, default='input_matrix.in', help='File name')


def createRandomMatrix(n):
    maxVal = 1000  # I don't want to get Java / C++ into trouble
    matrix = []
    for i in range(n):
        matrix.append([random.randint(0, maxVal) for el in range(n)])
    return matrix

def create2DIndexMatrix(n, indexN):
    matrix = []
    for i in range(indexN):
        matrix.append([random.randint(0, n) for el in range(2)])
    return matrix


def saveMatrix(matrixA, matrixB, filename):
    if os.path.exists(filename): 
        os.remove(filename)
    else:   
        print("New file created: ",filename)
    f = open(filename, "w")
    for i, matrix in enumerate([matrixA, matrixB]):
        if i != 0:
            f.write("\n")
        for line in matrix:
            #pdb.set_trace()
            f.write("\t".join(map(str, line)) + "\n")


def saveCSRMatrix(CSR_matrix, filename, lines):
    if os.path.exists(filename): 
        os.remove(filename)
    else:   
        print("New file created: ",filename)

    f = open(filename,"w")
    f.write(str(lines))
    f.write("\n")
    for row, col in zip(*CSR_matrix.nonzero()):
        val = CSR_matrix[row,col]
        f.write("Row: "+str(row)+", Col: ")
        f.write(str(col)+", ")
        f.write("Val: "+str(val)+".")
        f.write("\n")
    f.close()

def main():
    global args, indexN
    args = parser.parse_args()
    print(40*"="+"\nArgs:{}\n".format(args)+40*"=")
   # random.seed(args.seed)
    random.seed()
    n = args.n
    numberOfElements = n*n
    indexN = random.randint(1, numberOfElements/2)
    outpath = args.dump
    #Create dense matrix
    matrixA = createRandomMatrix(n)
    matrixB = create2DIndexMatrix(n,indexN)
    #print(matrixA)
    #Convert to sparse matrix by replacing value below threshold to 0
    if (args.sparsity):
        #Replace random x %element to 0 in matrixA
        matrixA = np.asarray(matrixA)
        indicesA = np.random.choice(np.arange(matrixA.size), replace=False,
                           size=int(matrixA.size * (args.sparsity/100)))
        flatA  = matrixA.flatten()
        flatA[indicesA] = 0
        #Reshape it back to square matrix    
        flatA = flatA.reshape(n,n)
        print(flatA)
        matrixA_csr = sparse.csr_matrix(flatA)
        #print(matrixA_csr)
        matrixA = flatA.tolist()
        csr_Amatrix = "csrA_"+args.dump
        saveCSRMatrix(matrixA_csr, csr_Amatrix, n)
  
    #Replace random x %element to 0 in matrixB
    matrixB = np.asarray(matrixB)
    flatB  = matrixB.flatten()
    #Reshape it back to square matrix    
    flatB = flatB.reshape(indexN,2)
    print(flatB)
    #print(matrixA_csr)
    matrixB_csr = sparse.csr_matrix(flatB)
    matrixB = flatB.tolist()
    csr_Bmatrix = "csrB_"+args.dump
    saveCSRMatrix(matrixB_csr, csr_Bmatrix, indexN)
    saveMatrix(matrixA, matrixB, args.dump)

if __name__ == '__main__':
    main()
