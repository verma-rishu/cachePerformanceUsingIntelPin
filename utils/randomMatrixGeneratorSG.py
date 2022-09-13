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
    nonDuplicateMatrix = []
    for i in range(indexN):
        matrix.append([random.randint(0, n-1) for el in range(2)])
    nonDuplicateMatrix = list(set(map(lambda i: tuple(sorted(i)), matrix)))
    return nonDuplicateMatrix

def create1DGatherMatrix(indexN):
    matrix = []
    for i in range(indexN):
        input = random.randint(1,1000)
        matrix.append(input)
    return matrix


def saveMatrix(inputMatrix, gatherIndexingVector, scatterIndexingVector, gatherMatrix, filename):
    if os.path.exists(filename): 
        os.remove(filename)
    else:   
        print("New file created: ",filename)
    f = open(filename, "w")
    for i, matrix in enumerate([inputMatrix, gatherIndexingVector, scatterIndexingVector, gatherMatrix]):
        if i != 0:
            f.write("\n")
        for line in matrix:
            #pdb.set_trace()
            f.write("\t".join(map(str, line)) + "\n")


def saveCSRMatrix(CSR_matrix, filename):
    if os.path.exists(filename): 
        os.remove(filename)
    else:   
        print("New file created: ",filename)

    f = open(filename,"w")
    f.write(str(args.n))
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

    #Creating input data matrix, indexing vectors (for scatter and gather both), matrix for gathered data
    inputMatrix = createRandomMatrix(n)
    gatherIndexingVector = create2DIndexMatrix(n,indexN)
    scatterIndexingVector = create2DIndexMatrix(n,len(gatherIndexingVector))
    gatherMatrix = create1DGatherMatrix(len(scatterIndexingVector))
    
    #Convert to sparse matrix by replacing value below threshold to 0
    if (args.sparsity):
        #Replace random x %element to 0 in inputMatrix
        inputMatrix = np.asarray(inputMatrix)
        indicesInputMatrix = np.random.choice(np.arange(inputMatrix.size), replace=False,
                           size=int(inputMatrix.size * (args.sparsity/100)))
        flatInputMatrix  = inputMatrix.flatten()
        flatInputMatrix[indicesInputMatrix] = 0
        #Reshape it back to square matrix    
        flatInputMatrix = flatInputMatrix.reshape(n,n)
        print(flatInputMatrix)
        inputMatrix_csr = sparse.csr_matrix(flatInputMatrix)
        inputMatrix = flatInputMatrix.tolist()
        csr_InputMatrix = "csrInputMatrix_"+args.dump
        saveCSRMatrix(inputMatrix_csr, csr_InputMatrix)
  
    #gatherIndexingVector
    gatherIndexingVector = np.asarray(gatherIndexingVector)  
    flatGatherIndexingVector  = gatherIndexingVector.flatten()
    flatGatherIndexingVector = flatGatherIndexingVector.reshape(len(gatherIndexingVector),2)
    print(flatGatherIndexingVector)
    gatherIndexingVector_csr = sparse.csr_matrix(flatGatherIndexingVector)
    gatherIndexingVector = flatGatherIndexingVector.tolist()
    csr_GatherIndexingVector= "csrGatherIndexingVector_"+args.dump
    saveCSRMatrix(gatherIndexingVector_csr, csr_GatherIndexingVector)

    #scatterIndexingVector
    scatterIndexingVector = np.asarray(scatterIndexingVector)
    flatScatterIndexingVector  = scatterIndexingVector.flatten()
    flatScatterIndexingVector = flatScatterIndexingVector.reshape(len(scatterIndexingVector),2)
    print(flatScatterIndexingVector)
    scatterIndexingVector_csr = sparse.csr_matrix(flatScatterIndexingVector)
    scatterIndexingVector = flatScatterIndexingVector.tolist()
    csr_ScatterIndexingVector = "csrScatterIndexingVector_"+args.dump
    saveCSRMatrix(scatterIndexingVector_csr, csr_ScatterIndexingVector)

    #gatherMatrix
    gatherMatrix = np.asarray(gatherMatrix)
    flatGatherMatrix  = gatherMatrix.flatten()
    flatGatherMatrix = flatGatherMatrix.reshape(1, len(gatherMatrix))
    print(flatGatherMatrix)
    gatherMatrix_csr = sparse.csr_matrix(flatGatherMatrix)
    gatherMatrix = flatGatherMatrix.tolist()
    csr_GatherMatrix = "csrGatherMatrix_"+args.dump
    saveCSRMatrix(gatherMatrix_csr, csr_GatherMatrix)

    saveMatrix(inputMatrix, gatherIndexingVector,scatterIndexingVector, gatherMatrix, args.dump)

if __name__ == '__main__':
    main()
