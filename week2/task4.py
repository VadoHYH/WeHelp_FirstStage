def get_number(index):
    final_num=0
    rule=[4,4,-1]
    for i in range(index):
        final_num+=rule[i%3]
    print (final_num)
    return final_num
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70