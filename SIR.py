from numpy.random import binomial
import matplotlib.pyplot as plt

'''
GROUPS:
    S: Susceptible
    I: Infected
    R: Recovered
'''

if __name__ == '__main__':
    # Population size
    N = 100000

    # P(S -> I)
    alpha = .0005

    # P(I -> R)
    beta = .05

    days = []
    for i in range(100):
        S = [N]
        I = [1]
        R = [0]
        t = 0

        # Run until all recovered or we run out of infected people
        while R[t] < (N + 1) and I[t] > 0:
            S.append(binomial(S[t], (1 - alpha) ** I[t]))
            R.append(R[t] + binomial(I[t], beta))
            I.append(N + 1 - S[t + 1] - R[t + 1])

            t += 1

        days.append(t)
    print(sum(days) / len(days))

    plt.plot(range(0, t + 1), S, color='red', label='Susceptible')
    plt.plot(range(0, t + 1), I, color='blue', label='Infected')
    plt.plot(range(0, t + 1), R, color='orange', label='Recovered')
    plt.legend()
    plt.show()
