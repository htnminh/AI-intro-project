from numpy import empty
from AI_intro_project import State
from Coordinate_and_Move import Coordinate, Move

'''
        _
    .__(.)<   (MEOW)
     \___)
~~~~~~~~~~~~~~~~~~~~~~~~~
'''
def _astar_heuristic(cur_pos: Coordinate):
    # TODO: this evening: implement that what the cat heuristic
    return


'''
A* search

exposed info:
----
  State.board_size       ||  tuple (m, n)
  State.walked_moves     ||  list (CnM.Move = (cur_x, cur_y, dir))
  State.current_pos      ||  CnM.Coordinate (cur_x, cur_y)
  State.current_tax      ||  float
  Goal                   ||  is always board_size - (1, 1); aka (m-1, n-1)

exposed func:
  State.check_not_duplicate_move  ->  bool
  State.available_moves_list      ->  list
  State.tax_after_move            ->  State.current_tax

'''
def astar(start: State):
    ''' instantiate basic vars '''
    # starting with f = 0
    #-- Doesn't matter if f = 0 or is calculated properly,
    #-- starting node will always be popped off. 
    #-- This merely works as a var-declaration for later stuff.
    start.f = 0

    # attach a parent node
    #-- this does nothing actually.
    #-- looks cool tho
    start.parent = None

    # opening nodes
    _open = []
    _open.append(start)

    # closed nodes
    _closed = []

    # goal node
    _goal = (start.board_size[0]-1, start.board_size[1]-1)

    # run A* until break;
    while _open:
        # get node with minimum f
        _min_f = min([node.f for node in _open])

        # pop the node with min f for expansion
        _current = _open.pop(_open.index(_min_f))

        # add that node to _closed
        _closed.append(_current)

        # stop if popped goal node
        if _current.current_pos == Coordinate(_goal):
            break

        # get available moves, continue if none is found
        if _current.available_moves_list() is empty:
            continue

        for _dir in _current.available_moves_list():
            # temporary node
            temp = _current
            temp_move = Move(
                temp.current_pos.x,
                temp.current_pos.y,
                _dir
            )
            temp.move_to_direction(temp_move)
            
            # current tax as g
            temp.g = temp.tax_after_move(temp_move) #TODO: need to convert to current_tax later
            
            # heuristic func as h
            #--> blame Nam for weird heuristic
            temp.h = _astar_heuristic(
                temp.current_pos
            )

            # A* function
            temp.f = temp.g + temp.h

            # check if node w/ better A* function f is available in _open
            t_do_continue = False
            for t_node in _open:
                if t_node.f < temp.f:
                    t_do_continue = True
                    break

            # ignore temp and expand this t_node instead
            if t_do_continue:
                continue

            # temp has great f, so add that to _open
            _open.append(temp)

            # attach parent node & moved dir to temp
            #-- like a linked list, hrmf..
            temp.parent = _current
            temp._dir = _dir

            # that TODO up there-----------------------^
            temp.current_tax = temp.g
        
    path = []
    while _current.parent is not None:
        path.append(_current._dir)
        _current = _current.parent

    return path[::-1]    

if __name__ == "__main__":
    _internalVar = State()
    astar(_internalVar)