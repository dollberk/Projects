

def printMatrix(m):
    for row in m:
        print(row)


def matrixMult(A, B):
    a_rows = len(A)
    a_cols = len(A[0])
    b_rows = len(B)
    b_cols = len(B[0])

    if a_cols == b_rows:
        product = [[0 for x in range(b_cols)] for y in range(a_rows)]
        for a in range(a_rows):
            for bc in range(b_cols):
                for br in range(b_rows):
                    product[a][bc] += A[a][br] * B[br][bc]

        print(product)
    else:
        print("Cannot multiply Matrices!")
        return None

# Test1
A = [[ 2, -3, 3],
    [-2, 6, 5],
    [ 4, 7, 8]]

B = [[-1, 9, 1],
    [ 0, 6, 5],
    [ 3, 4, 7]]

C = matrixMult(A, B)
if not C == None:
    printMatrix(C)

# Test2

A = [[ 2, -3, 3, 0],
    [-2, 6, 5, 1],
    [ 4, 7, 8, 2]]

B = [[-1, 9, 1],
    [ 0, 6, 5],
    [ 3, 4, 7]]

C = matrixMult(A, B)
if not C == None:
    printMatrix(C)

# Test3
A = [[ 2, -3, 3, 5],
    [-2, 6, 5, -2]]

B = [[-1, 9, 1],
    [ 0, 6, 5],
    [ 3, 4, 7],
    [ 1, 2, 3]]
C = matrixMult(A, B)
if not C == None:
    printMatrix(C)