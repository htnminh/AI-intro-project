# -------------------------------------------------------------


from AI_intro_project.Coordinate_and_Move \
                import Coordinate, Move

from random import choice

import matplotlib.pyplot as plt

class State():
    '''a state of the game'''

    def __init__(self) -> None:
        '''
        Each state is composed by 4 components, which are:
        - board_size: a tuple (m, n)
        - walked_moves: a list of instances of Move,
          each instance is represented by (x, y,
          direction)
        - current_pos: Coordinate(x, y)
        - current_tax: a real number
        Properties:
        Methods:
        - initialize_4x4_default
        - initialize_6x6_default
        - initialize_8x8_default
        - initialize_mxn_default: pick a random state in the state
          directory
        - _plt_prepare: prepare matplotlib.pyplot for the game 
          visualizer
        - visualize: plot the board using matplotlib.pyplot (no
          subplot involved)
        - random_play: legally play several random moves
        - undo_last_move: undo last move
        - check_duplicate_move: check if a move is available
          for later walk
        - available_moves_list: a list of avalable moves
        - tax_after_move: the tax after a specified move
        - move_on_move: (wtf name) move the pilgrim on a
          move specified
        - move_to_direction: move the pilgrim to a specified
          direction (R, L, U, D)
        '''
        self.initialize_4x4_default()

    def initialize_mxn_blank(self, size=(4,4)) -> None:
        '''Initialize the state without moves'''
        self.board_size = size
        self.walked_moves = list()
        self.current_pos = Coordinate(0, 0)
        self.current_tax = 0.0

    def initialize_4x4_default(self) -> None:
        '''
        Initialize the state which is the same as the
        TED-Ed's video: https://youtu.be/6sBB-gRhfjE
        '''
        self.initialize_mxn_blank()

        # move to the right twice
        for _ in range(2):
            self.move_to_direction('R')

    def initialize_6x6_default(self) -> None:
        '''Initialize the state'''
        self.initialize_mxn_blank((6, 6))

        # move to the right twice
        for _ in range(3):
            self.move_to_direction('R')

    def initialize_8x8_default(self) -> None:
        '''Initialize the state'''
        self.initialize_mxn_blank((8, 8))

        # move to the right twice
        for _ in range(4):
            self.move_to_direction('R')

    def initialize_mxn_random(self) -> None:
        '''Initialize the state by a randomized state'''
        from AI_intro_project._Utilities import _Utilities
        s = _Utilities().load_randomly(
                sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
                directory='AI_intro_project/randomized_states',
                extension='state'
            )

        self.board_size = s.board_size
        self.walked_moves = s.walked_moves
        self.current_pos = s.current_pos
        self.current_tax = s.current_tax

    def _plt_prepare(self, show_move_numbers=True) -> None:
        '''
        Prepare matplolib.pyplot for plotting
        Used to visualize the current state in matplotlib
        Most of the things below are reversed in some way,
        since the x coordinate of the game is the y
        coordinate in math, etc.
        '''
        # move x axis to the top
        plt.rcParams['xtick.bottom'] = \
            plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = \
            plt.rcParams['xtick.labeltop'] = True
        
        # black board 
        for i in range(self.board_size[1] + 1):
            plt.plot(
                    [i,i],
                    [0,self.board_size[0]],
                    color='silver'
            )
        for i in range(self.board_size[0] + 1):
            plt.plot(
                    [0,self.board_size[1]],
                    [i,i],
                    color='silver'
            )

        # moves
        for index, move in enumerate(self.walked_moves):
            plt.plot(
                [move.coordinate_start.y,
                        move.coordinate_end.y],
                [move.coordinate_start.x,
                        move.coordinate_end.x],
                color='red'
            )
            if show_move_numbers:
                plt.text(move.coordinate_start.y/2 + move.coordinate_end.y/2,
                        move.coordinate_start.x/2 + move.coordinate_end.x/2,
                        index,
                        ha='center',
                        va='center',
                        fontfamily='monospace',
                        color='blue'
                        )
        # current tax text
        plt.text(
                self.board_size[1]/2,
                self.board_size[0]+3/4,
                f'Current tax: {self.current_tax}',
                ha='center',
                va='center',)

        # limit the plot by board size
        plt.xlim(-1, self.board_size[1] + 1)
        plt.ylim(-1, self.board_size[0] + 1)

        # invert y axis (oriented downward)
        plt.gca().invert_yaxis()

        # scale axes equally, so squares are displayed
        plt.gca().set_aspect('equal', adjustable='box')

        # show every value on the axes, and exclude -1
        plt.xticks([x for x in range(self.board_size[1] + 1)])
        plt.yticks([y for y in range(self.board_size[0] + 1)])

        # show
        plt.plot()

    def visualize(self, show_move_numbers=True) -> None:
        '''
        Visualize the current state in matplotlib
        '''
        self._plt_prepare(show_move_numbers=show_move_numbers)
        plt.show()

    def random_play(self, number_of_moves=20, silent=False) -> None:
        '''
        Randomly continue playing the current state
        for the given number of moves if the moves is
        possible
        Print the moves if silent is False
        '''
        for i in range(number_of_moves):
            if len(self.available_moves_list()) != 0:
                move = choice(self.available_moves_list())
                self.move_on_move(move)
                if not silent:
                    print(f'{move.__str__(show_coordinate_end=True)}, tax after move = {self.current_tax}')

    def undo_last_move(self) -> None:
        '''Undo the last move'''
        assert self.walked_moves, \
                'NO MOVE LEFT TO UNDO'
        last_move = self.walked_moves.pop(-1)
        recover_direction = last_move.reverse_direction()
        self.move_to_direction(recover_direction)
        self.walked_moves.pop(-1)

    def check_not_duplicate_move(self, move) -> bool:
        '''
        Check if a move is available for later walk, by
        checking if the move is already in walked_moves
        of the current state, return False if it
        is duplicated
        '''
        for walked_move in self.walked_moves:
            if walked_move == move:
                return False
        return True

    def available_moves_list(self) -> list():
        '''
        Return a list of instances of Move, which are the
        moves that the pilgrim can walk in the current state,
        by checking all 4 directions around the current_pos.
        '''
        result = list()
        for direction in ['L', 'U', 'R', 'D']:
            move = Move(self.current_pos.x,
                        self.current_pos.y,
                        direction)
            if (self.check_not_duplicate_move(move)
                    and move.check_inside(*self.board_size)):
                result.append(move)
        return result

    def tax_after_move(self, move) -> None:
        '''Return the tax after a move'''
        if move.direction == 'R':
            return self.current_tax + 2
        elif move.direction == 'L':
            return self.current_tax - 2
        elif move.direction == 'U':
            return self.current_tax / 2
        elif move.direction == 'D':
            return self.current_tax * 2

    def move_on_move(self, move) -> None:
        '''perform the move on a Move instance'''
        assert move in self.available_moves_list(), \
                f'{move}: CANNOT MOVE THIS WAY'

        self.walked_moves.append(move)
        self.current_pos = move.coordinate_end
        self.current_tax = self.tax_after_move(move)
    
    def move_to_direction(self, direction) -> None:
        '''
        perform the move from the current position 
        to a direction
        '''
        self.move_on_move(
                Move(
                        self.current_pos.x,
                        self.current_pos.y,
                        direction
                )
        )


# Run this file to randomly move 20 times if available,
# print the moves, then visualize the final state
if __name__ == '__main__':  
    s = State()
    s.random_play()
    s.visualize()
