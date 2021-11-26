# -------------------------------------------------------------


from AI_intro_project.Coordinate_and_Road \
                import Coordinate, Road


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
        self.walked_roads = list()
        self.current_pos = Coordinate(0, 0)
        self.current_tax = 0

        # move to the right twice
        self.move(Road(
                self.current_pos.x, self.current_pos.y, 'R'))
        self.move(Road(
                self.current_pos.x, self.current_pos.y, 'R'))
        

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

    def tax_after_move(self, road):
        if road.direction == 'R':
            return self.current_tax + 2
        elif road.direction == 'L':
            return self.current_tax - 2
        elif road.direction == 'U':
            return self.current_tax / 2
        elif road.direction == 'D':
            return self.current_tax * 2

    def move(self, road):
        self.walked_roads.append(road)
        self.current_pos = road.coordinate_end
        self.current_tax = self.tax_after_move(road)


