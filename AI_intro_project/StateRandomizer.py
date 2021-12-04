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

import pickle as pkl
import random
from math import floor, ceil, sqrt
from pathlib import Path

from AI_intro_project.State import State


class _StateUtilities():
    '''
    only used to do certain things of a state,
    given some input specified
    NOT AN INHERITANCE OF THE State CLASS
    '''
    def __init__(        # dependencies
                self,
                state=None,
                m=None,  # state
                n=None,  # state
                file_name=None,  # m, n, suffix_index, directory
                file_path=None,  # m, n, suffix_index, directory
                directory=None,  
                suffix_index=None,
                extension=None,
                sizes=None
        ):
        self.state = state
        self.m, self.n = m, n
        self.file_name = file_name
        self.file_path = file_path
        self.directory = directory
        self.suffix_index = suffix_index
        self.extension = extension
        self.sizes = sizes

        if self.state is not None:
            self.set_m_n()
        
        if self.m is not None and self.n is not None \
                    and self.suffix_index is not None and self.directory is not None:
                self.set_file_name_file_path()

    def set_m_n(self):
        '''
        GIVEN: state
        Set m, n
        '''
        self.m, self.n = self.state.board_size
    
    def set_file_name_file_path(self):
        '''
        GIVEN: m, n, suffix_index, directory, file_name
        Set file_name, file_path
        '''
        self.file_name = f'{self.m}x{self.n}_{self.suffix_index}'
        self.file_path = f'{self.directory}/{self.file_name}.{self.extension}'

    def numbers_of_moves_calc(self):
        '''
        GIVEN: m, n
        Calculate the number of forced moves
        '''
        return floor(sqrt(self.m*self.n)/2), \
                ceil(sqrt(self.m*self.n)/2)

    def save(self):
        '''
        GIVEN: file_path
        save
        '''
        with open(self.file_path, 'wb') as f:
            pkl.dump(self.state, f)

    def load(self):
        '''
        GIVEN: file_path
        load state in file_path, assign some properties to
        self, return the state
        '''
        with open(self.file_path, 'rb') as f:
            self.state = pkl.load(f)
            self.set_m_n()
        return self.state
    
    def load_and_visualize(self):
        '''
        GIVEN: file_path
        load it, then visualize it
        '''
        self.load()
        self.state.visualize()
    
    def visualize_all(self):
        '''
        GIVEN: sizes, directory, extension
        visualize all states
        '''
        for m, n in self.sizes:
            for suffix_index in range(2):
                self.m, self.n = m, n
                self.suffix_index = suffix_index
                self.set_file_name_file_path()
                self.load_and_visualize()

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
            _StateUtilities(state=s, directory=self.directory,
                            suffix_index=suffix_index, extension=self.extension).save()
            
        return s
            
    def randomize_all(self, save=False):
        for size in self.sizes:
            number_of_moves_0, number_of_moves_1 = \
                    _StateUtilities(m=size[0], n=size[1]).numbers_of_moves_calc()
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
    _StateUtilities(
        directory=directory,
        extension='state',
        sizes=[(i,j) for i in range(4,9) for j in range(4,9)]).visualize_all()
    
