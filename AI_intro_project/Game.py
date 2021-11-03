# TODO: write tests for this file
# TODO: rearrange and write descriptions for methods and
#       properties
# -------------------------------------------------------------

'''
self-note:

x and y in this project are not of normal coordinate system
in mathematics, instead they point out the coordinate in
the form of a 2D numpy array like this:

(0,0) (0,1) (0,2) ... (0,n)
(1,0) (1,1) (1,2) ... (1,n)
                   .
                   .
                   .
(m,0) (m,1) (m,2) ... (m,n)
'''


class Coordinate():
    '''a coordinate instance of the game'''

    def __init__(self, x, y):
        '''
        Each coordinate is composed by 2 components, x and y
        '''
        self.x = x
        self.y = y

    def __str__(self):
        '''String represent: Coordinate(x, y)'''
        return 'Coordinate(%s, %s)' % (self.x, self.y)

    def check_inside(self, m, n):
        '''
        Return False if the coordinate is out-of-bounds of
        the board which has the size (m, n), or return True
        if it is inside the board
        '''
        if 0 <= self.x <= m and 0 <= self.y <= n:
            return True
        return False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Road():
    '''a road instance of the game'''

    def __init__(self, x, y, direction):
        '''
        Each road is composed by 3 components, which are:
        - x and y: 2 real numbers
        - direction: a character, which is one of the 4
          characters 'R', 'L', 'U' or 'D'
        Properties:
        - coordinate_start: the coordinate before moving
        - coordinate_end: the coordinate after moving
        Methods:
        - coordinate_end_calc: calculate the coordinate_end
        '''
        self.coordinate_start = Coordinate(x, y)
        self.direction = direction
        self.coordinate_end = self.coordinate_end_calc()

    def __str__(self) -> str:
        return 'Road(%s, %s, %s)' % (
            self.coordinate_start.x,
            self.coordinate_start.y,
            self.direction
        )

    def coordinate_end_calc(self) -> Coordinate:
        '''
        Return a tuple of the form (x, y), which is the
        coordinate after moving on the road.
        '''
        if self.direction == 'R':
            return Coordinate(
                self.coordinate_start.x,
                self.coordinate_start.y + 1)
        if self.direction == 'L':
            return Coordinate(
                self.coordinate_start.x,
                self.coordinate_start.y - 1)
        if self.direction == 'U':
            return Coordinate(
                self.coordinate_start.x - 1,
                self.coordinate_start.y)
        if self.direction == 'D':
            return Coordinate(
                self.coordinate_start.x + 1,
                self.coordinate_start.y)

    def __eq__(self, other) -> bool:
        '''
        Return if self and other are the same road.
        They are the same road if the 2 coordinates (start
        and end) of each road are pair-wise equal between them.
        '''
        if (self.coordinate_start == other.coordinate_start and
                self.coordinate_end == other.coordinate_end):
            return True
        elif (self.coordinate_start == other.coordinate_end and
              self.coordinate_end == other.coordinate_start):
            return True
        else:
            return False

    def check_inside(self, m, n):
        '''
        Return True if the road is out-of-bounds of
        the board which has the size (m, n)
        '''
        return (self.coordinate_start.check_inside(m, n) and
                self.coordinate_end.check_inside(m, n))


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
        self.available_roads = self.available_roads_calc()

    def __str__(self):
        '''
        TODO
        '''
        pass

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
        self.walked_roads = [
            Road(0, 0, 'R'),
            Road(0, 1, 'R'),
        ]
        self.current_pos = Coordinate(0, 2)
        self.current_tax = 4

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

    def available_roads_calc(self):
        '''
        Return a list of instances of Road, which are the roads
        that the pilgrim can walk in the current state,
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
