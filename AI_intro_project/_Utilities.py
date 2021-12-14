from math import floor, ceil, sqrt
import pickle as pkl
import random

from AI_intro_project.State import State


class _Utilities():
    '''
    only used to do certain things,
    given some input specified
    '''
    def __init__(self) -> None:
        pass

    def numbers_of_moves_calc(self, size) -> tuple[int, int]:
        '''
        GIVEN: size
        calculate the number of forced moves of the 2 boards
        '''
        m, n = size
        return floor(sqrt(m*n)/2), \
                ceil(sqrt(m*n)/2)

    def save(self, state, file_path) -> None:
        '''
        GIVEN: state, file_path
        save state in file_path
        '''
        with open(file_path, 'wb') as f:
            pkl.dump(state, f)

    def load(self, file_path) -> State:
        '''
        GIVEN: file_path
        load state in file_path, return the state
        '''
        with open(file_path, 'rb') as f:
            s = pkl.load(f)
        return s
    
    def load_randomly(self, sizes, directory, extension) -> State:
        '''
        GIVEN: sizes, directory, extension
        return any state in the directory, randomly
        '''
        m, n = random.choice(sizes)
        suffix_index = random.choice([0, 1])
        
        file_name = f'{m}x{n}_{suffix_index}.{extension}'
        file_path = f'{directory}/{file_name}'

        s = self.load(file_path=file_path)
        return s
    
    def load_and_visualize(self, file_path) -> None:
        '''
        GIVEN: file_path
        load the state in file_path, then visualize it
        '''
        s = self.load(file_path)
        s.visualize()
    
    def visualize_all(self, sizes, directory, extension) -> None:
        '''
        GIVEN: sizes, directory, extension
        visualize all states in the directory
        '''
        print('CTRL-C TO EXIT, OR SEE ALL THE 50 STATES IF YOU WANT')

        for m, n in sizes:
            for suffix_index in [0, 1]:
                file_name = f'{m}x{n}_{suffix_index}.{extension}'
                file_path = f'{directory}/{file_name}'

                self.load_and_visualize(file_path=file_path)

    def load_all(self, sizes, directory, extension) -> list[State]:
        '''
        GIVEN: sizes, directory, extension
        return a list of all states in the directory
        '''
        res = list()
        for m, n in sizes:
            for suffix_index in [0, 1]:
                file_name = f'{m}x{n}_{suffix_index}.{extension}'
                file_path = f'{directory}/{file_name}'
                s = self.load(file_path=file_path)
                res.append(s)
        return res


if __name__ == '__main__':
    # an example with method load_all()
    _Utilities().visualize_all(
        sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
        directory='AI_intro_project/randomized_states',
        extension='state'
    )
