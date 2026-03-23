class A:
    p = 10
    def pepa():
        return 1
    def pupa():
        return 0

class B:
    a = 12

aee = A()
bee = B()

print([ x for x in dir(aee) if '__' not in x and callable(getattr(aee, x))])

index = [x for x in range(2)]



iterator = iter(index)

print(next(iterator))
print(next(iterator))
print(next(iterator))