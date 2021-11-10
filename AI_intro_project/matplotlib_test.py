import matplotlib.pyplot as plt

# board
for i in range(5):
    plt.plot(
            [i,i],
            [0,4],
            color='black'
    )
for i in range(5):
    plt.plot(
            [0,4],
            [i,i],
            color='black'
    )

# walked_roads
plt.plot([0,2],
         [0,0],
         color='red')

# limit by board_size
plt.xlim(-1, 5)
plt.ylim(-1, 5)
plt.gca().invert_yaxis()
plt.gca().set_aspect('equal', adjustable='box')

plt.plot()
plt.show()