from numpy.random import binomial
import matplotlib.pyplot as plt
import math

'''
GROUPS:
    S: Susceptible
    E: Exposed --- NOTE: Exposed means infected, but not contagious
    I: Infected
    R: Recovered
    M: Masked
    D: Deceased
'''

# REFERENCE THIS LINK FOR INFO ON SEIR: https://docs.idmod.org/projects/emod-hiv/en/latest/model-seir.html

if __name__ == '__main__':
    # Population size
    N = 100000

    # Mask adoption rate. Determines how many start in S vs M
    # Hi, avg, low: .2, .5, .9 for each
    mask_adoption = .2
    mask_effectiveness = .2

    # P(S -> E)
    r0 = 2.7        # avg number of people an infected person will spread to, scale by pop to get "per person" avg
    alpha = r0/N

    #P(M -> E)
    alpha_m = alpha*(1-mask_effectiveness)

    # P(E -> I) -- set as .375 because it usually takes 2-4 days to become infectious?
    # should think ab this a bit more
    exposed_rate = .375

    # P(I -> R)
    beta = .1

    # P(I -> D)
    recovery_rate = .97  # somewhere between [.97, .9975]
    death_rate = 1 - recovery_rate

    #ICU info
    icu_beds = 27
    icu_rate = .001782

    days = []
    deaths = []
    days_til_peak = []
    peak_infections = 1
    for i in range(100):

        # for debugging
        N_list = [N]

        S = [N*(1-mask_adoption)-1]
        M = [N*mask_adoption]
        E = [0]
        I = [1]
        R = [0]
        D = [0]
        t = 0

        # Run until all recovered or we run out of infected/exposed people
        while (I[t] > 0 or E[t] > 0):
            S.append(binomial(S[t], (1 - alpha) ** I[t]))
            M.append(binomial(M[t], (1 - alpha_m)**I[t]))

            # since the path from I could go to R or D, we first calculate the num that go to R or D
            num_leaving_I = binomial(I[t], beta)

           # lower recovery if ICU full
            if I[t]*icu_rate > icu_beds:
                recovery_rate = .9
            else:
                recovery_rate = .97

            I_to_R = math.ceil(num_leaving_I * recovery_rate)
            I_to_D = num_leaving_I - I_to_R

            # transitioning num leaving I to R or D
            R.append(R[t] + I_to_R)
            D.append(D[t] + I_to_D)

            I.append(binomial(E[t], exposed_rate))


            # NOTE: formula for E is what the formula for I was under the SIR model
            E.append(N - S[t + 1] - I[t + 1] - R[t + 1] - D[t + 1] - M[t + 1])

            # adjusting

            # need to make sure S + R + D + I + V == N
            N_list.append(S[t] + E[t] + R[t] + D[t] + I[t] + M[t])

            if I[-1] > peak_infections:
                peak_infections = I[-1]
                peak_day = t 

            t += 1

        days.append(t)
        days_til_peak.append(peak_day)
        deaths.append(D[-1])

    print(sum(days) / len(days), 'avg days')
    print(sum(deaths)/len(deaths), 'avg deaths')
    print(sum(days_til_peak)/len(days_til_peak), 'avg days til peak')

    plt.figure(figsize=(15, 5))
    plt.plot(range(0, t + 1), S, color='red', label='Susceptible Unmasked')
    plt.plot(range(0, t + 1), E, color='green', label='Exposed')
    plt.plot(range(0, t + 1), I, color='blue', label='Infected')
    plt.plot(range(0, t + 1), R, color='orange', label='Recovered')
    plt.plot(range(0, t + 1), M, color='plum', label='Susceptible Masked')
    plt.plot(range(0, t + 1), D, color='black', label='Deceased')
    plt.legend()
    plt.show()