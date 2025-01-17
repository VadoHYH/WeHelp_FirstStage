def find(spaces, stat, n):
    best_index=-1
    for i in range(len(stat)):
        if stat[i]==1:
            if spaces[i]==n:
                best_index=i
            elif spaces[i]>n:
                if spaces[i]<spaces[(i-1)]:
                    best_index=i    
    print(best_index)
find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2