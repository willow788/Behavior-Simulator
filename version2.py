import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#setting the grid size
N=20

#setting the variables
stress = np.random.rand(N, N)*0.4
focus = 1 - stress
energy = np.ones((N, N))

#Extra behavioral traits to create different type of agents
resilience = np.random.rand(N, N) #how can handle the stress, inversly prop to stress
influence = np.random.rand(N, N) #how much they affect others

stress_spread_rate = 0.5
recovery_rate = 0.003


fig, ax = plt.subplots()
mat = ax.matshow(stress, cmap='plasma', vmin=0, vmax=1)
plt.colorbar(mat)

def update(frame):
    global stress, focus, energy

    #new stress is just the copy of the previously initialised stress
    new_stress = stress.copy()

    if frame % 30 == 0 :
        x, y = np.random.randint(0, N, 2)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x+dx < N and 0 <= y+dy < N:
                    stress[x+dx][y+dy] += 0.8
                    #increasing some stress randomly


    if frame == 100:
        stress += 0.4



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
                    new_stress[i][j] += stress_spread_rate * n * influence[i][j]
                    #influencers will influence more 

                #recovery formula-- new formula - highly resilient agents will recover fast
                new_stress[i][j] -= recovery_rate * energy[i][j] * resilience[i][j]

            



    #clamp values between 1
    stress = np.clip(new_stress, 0, 1)

    #update dependent states
    focus = 1 - stress
    energy = np.clip(energy + 0.01 - stress * 0.02, 0, 1)

    mat.set_data(stress)
    return [mat]

ani = animation.FuncAnimation(fig, update, frames=300, interval=2500, repeat=False)
plt.title("Behavioural simulator: stress spread with multi-behavioral agents")
plt.show()






