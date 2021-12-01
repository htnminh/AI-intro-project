# -------------------------------------------------------------


from AI_intro_project.Coordinate_and_Road \
                import Coordinate, Road

from random import choice

import matplotlib.pyplot as plt


class State():
    '''a state of the game'''

    def __init__(self):
        '''
        Each state is composed by 4 components, which are:
        - board_size: a tuple (m, n)
        - walked_roads: a list of instances of Road,
          each instance is represented by (x, y,
          direction)
        - current_pos: Coordinate(x, y)
        - current_tax: a real number
        Properties:
        - available_roads: a list of instances of Road,
          which are the roads that the pilgrim can walk
          in the current state
        Methods:
        - random_initialize: randomize the initial state
        - _fixed_initialize: (development only)
          initialize the TED-Ed's state
        - check_duplicate_road: check if a road is
          available for later walk
        - available_roads_calc: calculate available_roads
        '''
        self._fixed_initialize()
        self.available_roads = self.available_roads_list()

    def random_initialize(self, seed):
        '''
        TODO
        Randomize the initial state, given the seed
        '''
        pass

    def _fixed_initialize(self):
        '''
        FOR DEVELOPMENT ONLY
        Initialize the state which is the same as the
        TED-Ed's video: https://youtu.be/6sBB-gRhfjE
        '''
        self.board_size = (4, 4)
        self.walked_roads = list()
        self.current_pos = Coordinate(0, 0)
        self.current_tax = 0.0

        # move to the right twice
        self.move_to_direction('R')
        self.move_to_direction('R')
        
    def plt_preparation(self, show_move_numbers=True):
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
        for index, road in enumerate(self.walked_roads):
            plt.plot(
                [road.coordinate_start.y,
                        road.coordinate_end.y],
                [road.coordinate_start.x,
                        road.coordinate_end.x],
                color='red'
            )
            if show_move_numbers:
                plt.text(road.coordinate_start.y/2 + road.coordinate_end.y/2,
                        road.coordinate_start.x/2 + road.coordinate_end.x/2,
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

    def visualize(self, show_move_numbers=True):
        '''
        Visualize the current state in matplotlib
        '''
        self.plt_preparation(show_move_numbers=show_move_numbers)
        plt.show()

    def random_play(self, number_of_moves=20, silent=False):
        '''
        Randomly continue playing the current state
        for the given number of moves if the moves is
        possible
        Print the moves if silent is False
        '''
        for i in range(number_of_moves):
            if len(self.available_roads_list()) != 0:
                road = choice(self.available_roads_list())
                self.move_on_road(road)
                if not silent:
                    print(f'{road.__str__(show_coordinate_end=True)}, tax after move = {s.current_tax}')

    def undo_last_move(self):
        '''Undo the last move'''
        assert self.walked_roads, \
                'NO MOVE LEFT TO UNDO'
        last_move = self.walked_roads.pop(-1)
        if last_move.direction == 'R':
            recover_direction = 'L'
        if last_move.direction == 'L':
            recover_direction = 'R'
        if last_move.direction == 'U':
            recover_direction = 'D'
        if last_move.direction == 'D':
            recover_direction = 'U'
        self.move_to_direction(recover_direction)
        self.walked_roads.pop(-1)

    def check_not_duplicate_road(self, road):
        '''
        Check if a road is available for later walk, by
        checking if the road is already in walked_roads
        of the current state, return False if it
        is duplicated
        '''
        for walked_road in self.walked_roads:
            if walked_road == road:
                return False
        return True

    def available_roads_list(self):
        '''
        Return a list of instances of Road, which are the
        roads that the pilgrim can walk in the current state,
        by checking all 4 directions around the current_pos.
        '''
        result = list()
        for direction in ['R', 'L', 'U', 'D']:
            road = Road(self.current_pos.x,
                        self.current_pos.y,
                        direction)
            if (self.check_not_duplicate_road(road)
                    and road.check_inside(*self.board_size)):
                result.append(road)
        return result

    def tax_after_move(self, road):
        if road.direction == 'R':
            return self.current_tax + 2
        elif road.direction == 'L':
            return self.current_tax - 2
        elif road.direction == 'U':
            return self.current_tax / 2
        elif road.direction == 'D':
            return self.current_tax * 2

    def move_on_road(self, road):
        assert road in self.available_roads_list(), \
                f'{road}: CANNOT MOVE THIS WAY, CANCELLED'

        self.walked_roads.append(road)
        self.current_pos = road.coordinate_end
        self.current_tax = self.tax_after_move(road)
    
    def move_to_direction(self, direction):
        self.move_on_road(
                Road(
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
