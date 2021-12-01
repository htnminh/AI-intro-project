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


class Move():
    '''a move instance of the game'''

    def __init__(self, x, y, direction):
        '''
        Each move is composed by 3 components, which are:
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

    def __str__(self, show_coordinate_end=False) -> str:
        return 'Move(%s, %s, %s)%s' % (
            self.coordinate_start.x,
            self.coordinate_start.y,
            self.direction,
            ' -> ' + str(self.coordinate_end) \
                if show_coordinate_end else ''
        )

    def coordinate_end_calc(self) -> Coordinate:
        '''
        Return a tuple of the form (x, y), which is the
        coordinate after moving on the move.
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
        Return if self and other are the same move.
        They are the same move if the 2 coordinates (start
        and end) of each move are pair-wise equal between them.
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
        Return True if the move is out-of-bounds of
        the board which has the size (m, n)
        '''
        return (self.coordinate_start.check_inside(m, n) and
                self.coordinate_end.check_inside(m, n))
