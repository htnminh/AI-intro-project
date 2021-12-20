import random as rd

import matplotlib.pyplot as plt

from AI_intro_project.State import State


if __name__ == '__main__':
    path = 'AI_intro_project/_generated_images'
    rd.seed(69420)

    s = State()

    s._plt_prepare()
    plt.savefig(path+'/0')

    plt.clf()

    for _ in range(2):
        s.move_to_direction('D')
    s.move_to_direction('L')
    s.move_to_direction('D')
    s.move_to_direction('R')
    for _ in range(2):
        s.move_to_direction('R')
    for _ in range(3):
        s.move_to_direction('U')
    s.move_to_direction('L')
    s.move_to_direction('D')
    for _ in range(3):
        s.move_to_direction('L')
    for _ in range(3):
        s.move_to_direction('D')
    for _ in range(4):
        s.move_to_direction('R')

    s._plt_prepare()
    plt.savefig(path+'/1')

    plt.clf()

    s = State()
    s.initialize_mxn_random()
    s._plt_prepare()
    plt.savefig(path+'/2')