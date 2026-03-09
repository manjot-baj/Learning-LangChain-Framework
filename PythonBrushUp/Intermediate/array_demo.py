from array import *

arr1 = array("i", [12, 1, 23, 12, 34])
arr2 = array(arr1.typecode, (n for n in arr1))

print(type(arr1))
print(arr1)
print(arr1.tolist())

arr1.append(88)
arr1.reverse()

arr1[2] = 54

print(arr1)
print(arr2)

for n in arr1:
    print(n)
