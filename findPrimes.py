import matplotlib.pyplot as plt


def findPrimes(primesLess, j):
    for i in primesLess:
        if j < i * i:
            break
        if j % i == 0:
            return primesLess
    primesLess.append(j)
    return primesLess


primesLess = []
N = int(pow(10, 7))
for j in range(2, N):
    primesLess = findPrimes(primesLess, j)
print(primesLess)
plt.hist(primesLess, bins=int(1000))
plt.show()
