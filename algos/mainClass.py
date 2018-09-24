from poissonDistribution import poissonDistribution as pD

results = {}

for i in range(4, 37):
    poisson = pD('../data/E1516.csv', i)
    poisson.mainMethod()
    print(i)
    raw_input()