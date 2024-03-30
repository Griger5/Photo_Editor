import numpy as np

def mergeByColor(tab, p, q, r, color):
    tab_A = np.copy(tab[p:q+1])
    tab_B = np.copy(tab[q+1:r+1])
    length_A = tab_A.shape[0]
    length_B = tab_B.shape[0]

    i_A, i_B, i = 0, 0, 0

    while i_A < length_A and i_B < length_B:
        if tab_A[i_A][color] <= tab_B[i_B][color]:
            tab[p+i] = tab_A[i_A]
            i_A += 1
        else:
            tab[p+i] = tab_B[i_B]
            i_B += 1
       
        i += 1

    while i_A < length_A:
        tab[p+i] = tab_A[i_A]
        i_A += 1
        i += 1

    while i_B < length_B:
        tab[p+i] = tab_B[i_B]
        i_B += 1
        i += 1


def mergeSortByColor(tab, p, r, color):
    if p < r:
        q = (p+r)//2
        
        mergeSortByColor(tab, p, q, color)
        mergeSortByColor(tab, q+1, r, color)

        mergeByColor(tab, p, q, r, color)


def mergeBySum(tab, p, q, r):
    tab_A = np.copy(tab[p:q+1])
    tab_B = np.copy(tab[q+1:r+1])
    length_A = tab_A.shape[0]
    length_B = tab_B.shape[0]
    tab_A_summed = np.sum(tab_A, axis=1)
    tab_B_summed = np.sum(tab_B, axis=1)

    i_A, i_B, i = 0, 0, 0

    while i_A < length_A and i_B < length_B:
        if tab_A_summed[i_A] <= tab_B_summed[i_B]:
            tab[p+i] = tab_A[i_A]
            i_A += 1
        else:
            tab[p+i] = tab_B[i_B]
            i_B += 1
       
        i += 1

    while i_A < length_A:
        tab[p+i] = tab_A[i_A]
        i_A += 1
        i += 1

    while i_B < length_B:
        tab[p+i] = tab_B[i_B]
        i_B += 1
        i += 1
    
def mergeSortBySum(tab, p, r):
    if p < r:
        q = (p+r)//2
        
        mergeSortBySum(tab, p, q)
        mergeSortBySum(tab, q+1, r)

        mergeBySum(tab, p, q, r)