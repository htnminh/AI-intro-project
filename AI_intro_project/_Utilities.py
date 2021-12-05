from AI_intro_project.State import State

from math import floor, ceil, sqrt
import pickle as pkl
import random

class _Utilities():
    '''
    only used to do certain things,
    given some input specified

    How to use:
        1. see the method you need to use
        2. see the GIVEN requirements
        3. create an _Utilities instance, pass the required parameters
        4. use it
    '''
    def __init__(                   # dependencies
                self,
                state=None,
                m=None,             # state
                n=None,             # state
                file_name=None,     # m, n, suffix_index, directory, extension
                file_path=None,     # m, n, suffix_index, directory, extension
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
            self._set_m_n()
        
        if self.m is not None and self.n is not None \
                    and self.suffix_index is not None and self.directory is not None \
                    and self.extension is not None:
                self._set_file_name_file_path()

    def _set_m_n(self):
        '''
        GIVEN: state
        Set m, n
        '''
        self.m, self.n = self.state.board_size
    
    def _set_file_name_file_path(self):
        '''
        GIVEN: m, n, suffix_index, directory, extension
        Set file_name, file_path
        '''
        self.file_name = f'{self.m}x{self.n}_{self.suffix_index}.{self.extension}'
        self.file_path = f'{self.directory}/{self.file_name}'

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
        or
        GIVEN: m, n, suffix_index, directory, extension
        save
        '''
        with open(self.file_path, 'wb') as f:
            pkl.dump(self.state, f)

    def load(self):
        '''
        GIVEN: file_path
        load state in file_path, assign m, n to
        self, return the state
        '''
        with open(self.file_path, 'rb') as f:
            self.state = pkl.load(f)
            self._set_m_n()
        return self.state
    
    def load_randomly(self):
        '''
        GIVEN: sizes, directory, extension
        return any state randomly in the directory
        '''
        self.m, self.n = random.choice(self.sizes)
        self.suffix_index = random.choice([0, 1])
        self._set_file_name_file_path()
        self.load()
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
        visualize all states in the directory
        '''
        print('CTRL-C TO EXIT, OR SEE ALL THE 50 STATES IF YOU WANT')

        for m, n in self.sizes:
            self.m, self.n = m, n

            for suffix_index in [0, 1]:
                self.suffix_index = suffix_index
                self._set_file_name_file_path()
                self.load_and_visualize()


if __name__ == '__main__':
    # an example with method visualize_all()
    u = _Utilities(
        sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
        directory='AI_intro_project/randomized_states',
        extension='state'
    )
    u.visualize_all()