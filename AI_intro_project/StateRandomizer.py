'''
The randomizing script (and class) for states

All randomized states will be saved in the directory
    AI_intro_project/randomized_states as binary
    files, named from "4x4_0" to "8x8_1", with the
    extension ".state" ...
because the first 2 states are of size 4x4, the next 2
    are of size 4x5, then 4x6, 4x7, 4x8, then 5x4, 5x5,
    and so on, until 8x8. (50 states in total)
All the states are randomized to make sure that there
    exist at least one way to reach the goal
    intersection in the lower-right corner, without
    considering the tax.

The numbers of "forced moves" of 2 states of size mxn
    are calculated as follows:
        the first state: floor(sqrt(m*n)/2)
        the second state: ceil(sqrt(m*n)/2)
    if the 2 numbers above are equal, the randomizer
        will make sure that 2 states are different

Below the classes are the guides  # TODO
'''

import random

from pathlib import Path

from AI_intro_project.State import State
from AI_intro_project._Utilities import _Utilities

class StateRandomizer():
    def __init__(
            self,
            SEED = 50,  
            directory='AI_intro_project/randomized_states',
            extension='state',
        ):
        '''
        To prevent randomizing accidentally, you must call
        the randomize method manually to start the process
        '''
        if SEED is not None:
            random.seed(SEED)

        self.directory = directory
        self.extension = extension

        self.sizes = [(i,j) for i in range(4,9)
                            for j in range(4,9)]

    def randomize_one(self, size, number_of_moves,
                      save=False, suffix_index='0'):
        '''
        Randomize a state, save it if required, then return it
        This make sure that player can go to the goal point...
            | side-note: the maximum number of moves is 4,
            | so the worst case would be a square around,
            | then there is no move left, we will check
            | for that.
        '''
        s = State()
        s.initialize_mxn_blank(size)

        while True:
            s.random_play(number_of_moves=number_of_moves, silent=True)
            if len(s.available_moves_list()):
                break

        if save:
            _Utilities(state=s, directory=self.directory,
                            suffix_index=suffix_index, extension=self.extension).save()
            
        return s
            
    def randomize_all(self, save=False):
        for size in self.sizes:
            number_of_moves_0, number_of_moves_1 = \
                    _Utilities(m=size[0], n=size[1]).numbers_of_moves_calc()
            s0 = self.randomize_one(size, number_of_moves_0, save, '0')

            while True:
                s1 = self.randomize_one(size, number_of_moves_1, save, '1')
                # print(s0.current_pos, s1.current_pos)
                if s0.current_pos != s1.current_pos:
                    break
            

if __name__ == '__main__':
    directory='AI_intro_project/randomized_states'

    # create folder if not exist
    Path(directory).mkdir(parents=True, exist_ok=True)  

    # run the below line if you want to randomize with the seed 50, then save all 
    StateRandomizer().randomize_all(save=True)


    # see a state
    # _StateUtilities(file_path=r'AI_intro_project\randomized_states\4x6_0.state').load_and_visualize()
    
    # see all states - ctrl-C to stop
    _Utilities(
        directory=directory,
        extension='state',
        sizes=[(i,j) for i in range(4,9) for j in range(4,9)]).visualize_all()
    
