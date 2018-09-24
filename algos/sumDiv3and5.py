def computeSum5and3(maximumNumber):
    sum = 0
    for i in range(0, maximumNumber):
        if any(i % n == 0 for n in range(3, 6, 2)):
            sum += i  

    return sum


print(computeSum5and3(1000))


def newCompute():
    sum3 = 0
    sum5 = 0
    sum15 = 0
    for i in range(0, 1000):
        if i % 3 == 0:
            sum3 += i
        if i % 5 == 0:
            sum5 += i
        if i % 15 ==0:
            sum15 += i

    print(sum3, sum5, sum15)
    print(sum3 + sum5 - sum15)
    print(((sum3+sum5) -sum15)/2)

newCompute()


