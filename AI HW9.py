# Kaitlyn Dollberg
# AI HW9

import random

def bin_packing(someObjects, c, w) :
    capacity = c
    # create list of just weights
    weights = w
    objects = someObjects

    k = len(weights)
    num_bins = 0
    remaining_bin_space = 0
    bin_weights = [0]*k
    bin_contents = [[] for i in range(10)]
    
    for j in range(k) :
        # if next object fits in bin, add it
        if remaining_bin_space >= weights[j] :
           remaining_bin_space = remaining_bin_space - weights[j]
           bin_weights[num_bins] = bin_weights[num_bins] + weights[j]
           bin_contents[num_bins].append(objects[j])
           
        else :
        # if next object does not fit in bin, create new bin and add it
            num_bins +=1
            remaining_bin_space = capacity - weights[j]
            bin_weights[num_bins] = bin_weights[num_bins] + weights[j]
            bin_contents[num_bins].append(objects[j])
            
            
    value = list(filter(lambda a: a != [], bin_contents))

    print("BIN PACKING")
    print("number of bins needed: ", num_bins)
    print("capacity of bins: ", list(filter(lambda a: a != 0, bin_weights)))
    for r in range(len(value)) :
        print("bin ", (r + 1), ': ', value[r])

################## BEST SUITED BIN PACKING ####################

def bin_packing_best(someObjects, c, w) :
    capacity = c
    # create list of just weights
    weights = w
    objects = someObjects
      
    k = len(weights)
    num_bins = 0
    remaining_bin_space = [0] *k
    bin_weights = [0] *len(remaining_bin_space)
    bin_contents = [[] for i in range(10)]
        
    for i in range(k) :
        j = 0
        min = capacity + 1
        best_bin = 0
        # find the best bin suited for each object. i.e. which bin has enough room remaining to
        # allow unplaced bins to fill it
        for j in range(num_bins) :
            if (remaining_bin_space[j] >= weights[i] and remaining_bin_space[j] - weights[i] < min) :
                best_bin = j
                min = remaining_bin_space[j] - weights[i]
        # add a new bin when an object cannot fit in current bins        
        if (min == capacity + 1) :
            remaining_bin_space[num_bins] = capacity - weights[i]
            # add object to list of list representing placement of each object
            bin_contents[num_bins].append(objects[i])
            num_bins += 1
        else :
            # place object into best suited bin
            remaining_bin_space[best_bin] = remaining_bin_space[best_bin] - weights[i]
            bin_contents[best_bin].append(objects[i])

    for m in range(num_bins) :
        # create list of total weights in each bin
        bin_weights[m] = capacity - remaining_bin_space[m]
        
    value = list(filter(lambda a: a != [], bin_contents))
    
    print("BEST SUITED BIN PACKING")
    print("number of bins needed: ", num_bins)
    print("capacity of bins: ", list(filter(lambda a: a != 0, bin_weights)))
    for r in range(len(value)) :
        print("bin ", (r + 1), ': ', value[r])

################# BEST SUITED BIN PACKING REVERSED ################

def bin_packing_best_reversed(someObjects, c) :
    capacity = c
    # create list of reversed weights
    weights = []
    objects = []
    for i in reversed(someObjects) :
        objects.append(i)
    for i in range(len(someObjects)) :
        value = objects[i]
        weights.append(value[1])
        
    k = len(weights)
    num_bins = 0
    remaining_bin_space = [0] *k
    bin_weights = [0] *len(remaining_bin_space)
    bin_contents = [[] for i in range(10)]
        
    for i in range(k) :
        j = 0
        min = capacity + 1
        best_bin = 0
        # find the best bin suited for each object. i.e. which bin has enough room remaining to
        # allow unplaced bins to fill it
        for j in range(num_bins) :
            if (remaining_bin_space[j] >= weights[i] and remaining_bin_space[j] - weights[i] < min) :
                best_bin = j
                min = remaining_bin_space[j] - weights[i]
        # add a new bin when an object cannot fit in current bins        
        if (min == capacity + 1) :
            remaining_bin_space[num_bins] = capacity - weights[i]
            # add object to list of list representing placement of each object
            bin_contents[num_bins].append(objects[i])
            num_bins += 1
        else :
            # place object into best suited bin
            remaining_bin_space[best_bin] = remaining_bin_space[best_bin] - weights[i]
            bin_contents[best_bin].append(objects[i])

    for m in range(num_bins) :
        # create list of total weights in each bin
        bin_weights[m] = capacity - remaining_bin_space[m]
        
    value = list(filter(lambda a: a != [], bin_contents))
    
    print("BEST SUITED BIN PACKING REVERSED")
    print("Reversed weights: ", weights)
    print("number of bins needed: ", num_bins)
    print("capacity of bins: ", list(filter(lambda a: a != 0, bin_weights)))
    for r in range(len(value)) :
        print("bin ", (r + 1), ': ', value[r])

###############

    
              
if __name__ == "__main__" :

    # (vertex, edge weight, connecting vertex)
    objects = [('o1', 8, 'o4'), ('o1', 4, 'o2'), ('o2', 5, 'o5'), ('o3', 3, 'o7'), ('o4', 2, 'o6'), ('o5', 9, 'o3'), ('o6', 1, 'o5'), ('o7', 3, 'o6')]
    weights = []
    #create list of weights
    for i in range(len(objects)) :
        value = objects[i]
        weights.append(value[1])
        
    # create random capacity
    capacity = random.randint(10, 20)
    print("Capacity of each bin is :", capacity)
    print("weights: ", weights)
    print()
    bin_packing(objects, capacity, weights)
    print("-----------------------------")
    bin_packing_best(objects, capacity, weights)
    print("-----------------------------")
    bin_packing_best_reversed(objects, capacity)
