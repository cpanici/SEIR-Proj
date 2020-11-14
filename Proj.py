from numpy.random import binomial
import matplotlib.pyplot as plt



'''
GROUPS:
    S: Susceptible
    M: Masked
    V: Vaccinated
    I: Infected
    R: Recovered

Do all of them together or model separately?
'''



if __name__ == '__main__':
    # Population size
    N = 100000
    
    # Mask adoption rate. Determines how many start in S vs M
    mask_adoption = .5
    mask_effectiveness = .5

    # P(S -> I)
    alpha = .0005
    # P(M -> I)
    alpha_m = alpha*(1-mask_effectiveness)
    
    #### Not sure about the E (Exposed) thing yet, can do that separately maybe or stick with this)
    # P(E -> I)
    #beta = .5

    #P(I -> R)
    beta = .05
    
    # With vaccinated, which approach?
    # Move vaccinated straight to R or do separate list like Masked 
    # and modify alpha based on vaccine effectiveness
    
    # Currently only includes SMIR, think about how we wanna do V and possible E
    days = []
    for i in range(100):
        S = [N*(1-mask_adoption)]
        M = [N*mask_adoption]
        I = [1]
        R = [0]
        t = 0

        # Run until all recovered or we run out of infected people
        while R[t] < (N + 1) and I[t] > 0:
            S.append(binomial(S[t], (1-alpha)**I[t]))
            M.append(binomial(M[t], (1-alpha_m**I[t])))
            R.append(R[t] + binomial(I[t], beta))
            I.append(N + 1 - S[t+1] - M[t+1] - R[t+1])

            t += 1
            
        days.append(t)
    print(sum(days)/len(days))


    plt.plot(range(0, t+1), S, color='red')
    plt.plot(range(0, t+1), M, color='green')
    plt.plot(range(0, t+1), I, color='blue')
    plt.plot(range(0, t+1), R, color='orange')
    plt.show()
