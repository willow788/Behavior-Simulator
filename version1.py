import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#setting a grid size
N = 20

#initialising states
stress = np.random.rand(N, N)*0.4
focus = 1 - stress
energy = np.ones((N, N))

#we have to spread the stress
stress_spread_rate = 0.5
recovery_rate = 0.003

fig, ax = plt.subplots()
mat = ax.matshow(stress, cmap='plasma', vmin=0, vmax=1)
plt.colorbar(mat)

def update(frame):
    global stress, focus, energy

    #new stress is just the copy of the previously initialised stress
    new_stress = stress.copy()

    #4 neighbour function
    for i in range(N):
        for j in range(N):
            neighbours = [] #initialised empty

            #case 1
            if i > 0:
                neighbours.append(stress[i-1][j]) #left

            if i < N-1:
                neighbours.append(stress[i+1][j]) #right

            if j > 0:
                neighbours.append(stress[i][j-1]) #up

            if j < N-1:
                neighbours.append(stress[i][j+1]) #down

            for n in neighbours:
                if n > 0.7:
                    new_stress[i][j] += stress_spread_rate * n

                #recovery formula
                new_stress[i][j] -= recovery_rate * energy[i][j]


    #clamp values between 1
    stress = np.clip(new_stress, 0, 1)

    #update dependent states
    focus = 1 - stress
    energy = np.clip(energy + 0.01 - stress * 0.02, 0, 1)

    mat.set_data(stress)
    return [mat]

ani = animation.FuncAnimation(fig, update, frames=300, interval=2500, repeat=False)
plt.title("Behavioural simulator: stress spread")
plt.show()




