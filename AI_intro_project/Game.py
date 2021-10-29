# TODO: write tests for this file
'''
A self-note:

x and y in this project are not of normal coordinate system in
mathematics, instead they point out the coordinate in the form
of a 2D numpy array like this:

(0,0) (0,1) (0,2) ... (0,n)
(1,0) (1,1) (1,2) ... (1,n)
                   .
                   .   
                   .
(m,0) (m,1) (m,2) ... (m,n)
'''

class Road():
    '''A road instance of the game'''
    def __init__(self, x, y, direction):
        '''
        A road is composed by 3 components, which are:
        - x and y: 2 real numbers
        - direction: A character, which is one of the 4
          characters 'R', 'L', 'U' or 'D'
        Properties:
        - coordinate_start: It is (x, y)
        - coordinate_end: The coordinate after moving
        Methods:
        - coordinate_end_calc: Calculate the coordinate_end
        '''
        self.x = x
        self.y = y
        self.direction = direction
        self.coordinate_start = (x, y)
        self.coordinate_end = self.coordinate_end_calc()

    def coordinate_end_calc(self) -> tuple:
        '''
        Return a tuple of the form (x, y), which is the
        coordinate after moving on the road.
        '''
        if self.direction == 'R':
            return (self.x, self.y + 1)
        if self.direction == 'L':
            return (self.x, self.y - 1)
        if self.direction == 'U':
            return (self.x - 1, self.y)
        if self.direction == 'D':
            return (self.x + 1, self.y)

    def __eq__(self, other) -> bool:
        '''
        Return if self and other are the same road.
        They are the same road if the 2 coordinates (start
        and end) of each road are pair-wise equal between them.
        '''
        if (        self.coordinate_start == other.coordinate_start
                and self.coordinate_end == other.coordinate_end):
            return True
        elif (      self.coordinate_start == other.coordinate_end
                and self.coordinate_end == other.coordinate_start):
            return True
        else:
            return False

class State():
    '''A state of the game'''
    def __init__(self):
        '''
        A state is composed by 4 components, which are:
        - board_size: A tuple (m, n)
        - walked_road: A list of instances of the class
        Road,  each instance is represented by (x, y, 
        direction)
        - current_pos: A tuple (x, y)
        - current_tax: A real number
        '''
        self.board_size = None
        self.walked_road = None
        self.current_pos = None
        self.current_tax = None
    
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
        self.walked_road = [
            Road(0, 0, 'R'),
            Road(0, 1, 'R'),
        ]
        self.current_pos = (0, 2)
        self.current_tax = 4
