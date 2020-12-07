from numpy.random import binomial
import matplotlib.pyplot as plt

'''
GROUPS:
    S: Susceptible
    E: Exposed --- NOTE: Exposed means infected, but not contagious
    I: Infected
    R: Recovered
    D: Deceased
'''

# REFERENCE THIS LINK FOR INFO ON SEIR: https://docs.idmod.org/projects/emod-hiv/en/latest/model-seir.html

if __name__ == '__main__':
    # Population size
    N = 10000

    # P(S -> E)
    alpha = .0005

    # P(E -> I) -- set as .375 because it usually takes 2-4 days to become infectious?
    # should think ab this a bit more
    exposed_rate = .375

    # P(I -> R)
    beta = .1

    # P(I -> D)
    recovery_rate = .97  # somewhere between [.97, .9975]
    death_rate = beta * (1 - recovery_rate)

    days = []
    for i in range(100):
        S = [N]
        E = [0]
        I = [1]
        R = [0]
        D = [0]
        t = 0

        # Run until all recovered or we run out of infected/exposed people
        while (R[t] < N + 1) and (I[t] > 0 or E[t] > 0):
            S.append(binomial(S[t], (1 - alpha) ** I[t]))
            R.append(R[t] + binomial(I[t], beta))
            D.append(D[t] + binomial(I[t], death_rate))
            I.append(binomial(E[t], exposed_rate))

            # NOTE: formula for E is what the formula for I was under the SIR model
            E.append(N + 1 - S[t + 1] - R[t + 1] - D[t + 1] - I[t + 1])


            t += 1

        days.append(t)
    print('Average Length in Days:', sum(days) / len(days))
    plt.figure(figsize=(15, 5))
    plt.plot(range(0, t + 1), S, color='red', label='Susceptible')
    plt.plot(range(0, t + 1), E, color='green', label='Exposed')
    plt.plot(range(0, t + 1), I, color='blue', label='Infected')
    plt.plot(range(0, t + 1), R, color='orange', label='Recovered')
    plt.plot(range(0, t + 1), D, color='black', label='Deceased')
    plt.legend()
    plt.show()
