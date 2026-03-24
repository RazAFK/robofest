class A:
    p = 10
    def pepa():
        return 1
    def pupa(self, a):
        return a+1
    def pupa(self, a, b, c):
        return a, b, c

class B:
    a = 12

aee = A()
bee = B()

print([ x for x in dir(aee) if '__' not in x and callable(getattr(aee, x))])

index = [x for x in range(2)]



iterator = iter(index)

print(next(iterator))
print(next(iterator))

print(aee.pupa(1))
print(aee.pupa(1, 2, 3))