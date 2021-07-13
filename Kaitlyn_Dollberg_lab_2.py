import random
from time import time
import pandas as pd


def mergeSort(L):
    if len(L) < 2:
        return L[:]
    else:
        mid = len(L)//2
        Left = mergeSort(L[:mid])
        Right = mergeSort(L[mid:])
        return merge(Left, Right)


def merge(A, B):
    out = []
    i, j = 0, 0
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            out.append(A[i])
            i += 1
        else:
            out.append(B[j])
            j += 1
    while i < len(A):
        out.append(A[i])
        i += 1
    while j < len(B):
        out.append(B[j])
        j += 1
    return out


def insertionSort(L):
    for i in range(1, n):
        key = A[i]
        j = i-1
        while j >=0 and A[j]>key:
            A[j+1] = A[j]
            j = j-1
        A[j+1] = key


def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


if __name__ == "__main__":

    total_times = [[0 for col in range(4)] for row in range(50)]
    count = 0
    for n in range(100, 5001, 100):
        A = [i for i in range(n)]
        random.shuffle(A)
        mtb = time()
        mergeSort(A)
        mta = time()
        mtime = round((mta - mtb)*1000, 5)

        random.shuffle(A)
        itb = time()
        insertionSort(A)
        ita = time()
        itime = round((mta - mtb)*1000, 5)

        random.shuffle(A)
        btb = time()
        bubble_sort(A)
        bta = time()
        btime = round((mta - mtb)*1000, 5)

        total_times[count][0] = n
        total_times[count][1] = mtime
        total_times[count][2] = itime
        total_times[count][3] = btime
        count += 1
    headers = ['N', 'MergeSort', 'InsertionSort', 'BubbleSort']
    time_df = pd.DataFrame(total_times, columns=headers)
    print(time_df)

