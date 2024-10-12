def union(arr1,arr2):
    union = []
    for i in arr1:  
        if i in union:
            union.append(i)
    
    for i in arr2:
        if i not in union:
            union.append(i)
    
    return union

arr1 = [1,2,5,6,7,8,9,10] 
arr2 = [1,2,3,4,5,6,3,4]

result=union(arr1,arr2)
print(result)