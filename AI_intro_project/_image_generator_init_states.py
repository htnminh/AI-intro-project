from AI_intro_project._Utilities import _Utilities
import matplotlib.pyplot as plt

states = _Utilities().load_all(
    sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
    directory='AI_intro_project/randomized_states',
    extension='state'
)

path = 'AI_intro_project/_initial_states_images/'
for index, state in enumerate(states):
    state._plt_prepare()
    plt.savefig(path + str(index).zfill(2))
    plt.clf()