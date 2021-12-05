from math import floor, ceil, sqrt
import pickle as pkl
import random

class Utilities():
    '''
    only used to do certain things,
    given some input specified
    NOT AN INHERITANCE OF THE State CLASS
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
            self.set_m_n()
        return self.state
    
    def load_randomly(self):
        '''
        GIVEN: sizes, directory, extension
        return the loaded state
        '''
        self.m, self.n = random.choice(self.sizes)
        self.suffix_index = random.choice([0, 1])
        self.set_file_name_file_path()
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
        visualize all states
        '''
        print('CTRL-C TO EXIT, OR SEE ALL THE 50 STATES IF YOU WANT')
        for m, n in self.sizes:
            for suffix_index in range(2):
                self.m, self.n = m, n
                self.suffix_index = suffix_index
                self.set_file_name_file_path()
                self.load_and_visualize()


if __name__ == '__main__':
    pass
