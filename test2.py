
def find_sum(n,current_sum,start,path):
    if current_sum == n:
        print(path)
    if current_sum > n:
        return
    for i in range(start,n):
        find_sum(n,current_sum+ i,i+1,path+[i])

find_sum(9,0,1,[])
