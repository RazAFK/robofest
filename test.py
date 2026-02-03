s = set()

s.add(sum)
s.add(max)
s.add(min)
arr = [1, 2, 3]

for func in s:
    print(func(arr))