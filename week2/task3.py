def func(*data):
    middle_name_counts={}
    for name in data:
        length = len(name)
        if length == 2 or length == 3:
            middle_name = name[1]
        else :
            middle_name = name[2] 

        middle_name_counts[middle_name]=middle_name_counts.get(middle_name,0)+1
        
    for name in data:
        length = len(name)
        if length == 2 or length == 3:
            middle_name = name[1]
        else :
            middle_name = name[2]
            
        if middle_name_counts[middle_name] == 1:
            print(name)
            return
    print("沒有")

func("彭大牆","陳王明雅","吳明")#print 彭大強
func("郭靜雅","王立強","郭林靜宜","郭立恆","林花花")#print林花花
func("郭宜雅","林靜宜","郭宜恆","林靜花")#print 沒有
func("郭宜雅","夏曼藍波安","郭宜恆")#print 夏曼藍波安