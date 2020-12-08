from numpy.random import binomial
import matplotlib.pyplot as plt
import math
import numpy as np

'''
GROUPS:
    S: Susceptible
    E: Exposed --- NOTE: Exposed means infected, but not contagious
    I: Infected
    R: Recovered
    V: Vaccinated
    D: Deceased
'''

# REFERENCE THIS LINK FOR INFO ON SEIR: https://docs.idmod.org/projects/emod-hiv/en/latest/model-seir.html

if __name__ == '__main__':
    # Population size
    N = 100000

    # P(S -> E)
    r0 = 2.7        # avg number of people an infected person will spread to, scale by pop to get "per person" avg
    alpha = r0/N

    # P(E -> I) -- set as .375 because it usually takes 2-4 days to become infectious?
    # should think ab this a bit more
    exposed_rate = .375

    # P(I -> R)
    beta = .1

    # P(I -> D)
    recovery_rate = .97  # somewhere between [.97, .9975]
    death_rate = 1 - recovery_rate

    # went with this value because it is unknown how many people can be vaccinated per day, but it would likely be at least
    # 1% of population
    num_vaccinated_per_day = N * .01

    # ICU info
    icu_beds = 27
    icu_rate = .001782

    days = []
    deaths = []
    days_til_peak = []
    peak_infections = 1
    for i in range(100):
        S = [N-1]
        E = [0]
        I = [1]
        R = [0]
        D = [0]
        V = [0]
        t = 0

        # Run until all recovered or we run out of infected/exposed people
        while (I[t] > 0 or E[t] > 0):
            S.append(binomial(S[t], (1 - alpha) ** I[t]))

            # since the path from I could go to R or D, we first calculate the num that go to R or D
            num_leaving_I = binomial(I[t], beta)
            I_to_R = math.ceil(num_leaving_I * recovery_rate)
            I_to_D = num_leaving_I - I_to_R

            # lower recovery if ICU full
            if I[t]*icu_rate > icu_beds:
                recovery_rate = .9
            else:
                recovery_rate = .97

            # transitioning num leaving I to R or D
            R.append(R[t] + I_to_R)
            D.append(D[t] + I_to_D)

            I.append(binomial(E[t], exposed_rate))

            # moving from S -> V
            if t < 250:
                V.append(0)

            else:
                # edge case if remainder of susceptible population gets vaccinated
                if S[t] <= num_vaccinated_per_day:
                    V.append(V[t] + S[t])
                    S[t + 1] = 0

                else:
                    V.append(V[t] + num_vaccinated_per_day)
                    S[t + 1] = S[t + 1] - num_vaccinated_per_day


            # NOTE: formula for E is what the formula for I was under the SIR model
            E.append(N - S[t + 1] - I[t + 1] - R[t + 1] - D[t + 1] - V[t + 1])

            if I[-1] > peak_infections:
                peak_infections = I[-1]
                peak_day = t 


            t += 1


        days.append(t)
        days_til_peak.append(peak_day)
        deaths.append(D[-1])

    print(sum(days) / len(days))

    avg_length = sum(days) / len(days)
    avg_deaths = sum(deaths) / len(deaths)
    avg_days_til_peak = sum(days_til_peak) / len(days_til_peak)

    plt.hist(days, bins=np.arange(min(days), max(days) + 20, 20))
    plt.title(f'Pandemic Length in Days (Avg: {avg_length})', size=15)
    plt.show()

    plt.hist(deaths, bins=np.arange(min(deaths), max(deaths) + 4, 4))
    plt.title(f'Total Deaths (Avg: {avg_deaths})', size=15)
    plt.show()

    plt.hist(days_til_peak)
    plt.title(f'Days Til Peak Infections (Avg: {avg_days_til_peak})', size=15)
    plt.show()

    # graph_label = {.2: 'Low', .5: 'Medium', .9: 'High'}
    # adoption_label = graph_label[mask_adoption]
    # effectiveness_label = graph_label[mask_effectiveness]

    plt.figure(figsize=(15, 5))
    plt.plot(range(0, t + 1), S, color='red', label='Susceptible')
    plt.plot(range(0, t + 1), E, color='green', label='Exposed')
    plt.plot(range(0, t + 1), I, color='blue', label='Infected')
    plt.plot(range(0, t + 1), R, color='orange', label='Recovered')
    plt.plot(range(0, t + 1), V, color='purple', label='Vaccinated')
    plt.plot(range(0, t + 1), D, color='black', label='Deceased')
    plt.title('Vaccine Only (No masks)')
    plt.legend()
    plt.show()
