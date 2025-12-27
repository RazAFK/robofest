tw = [2**x for x in range(1, 7)]
tr = [3**x for x in range(1, 5)]
t2 = 0
for i in tw:
    for x in range(i, 101, i):
        t2+=1
print(t2)
t3 = 0
for i in tr:
    for x in range(i, 101, i):
        t3+=1
print(t3)

print(2**(100-t2)*3**(100-t3))