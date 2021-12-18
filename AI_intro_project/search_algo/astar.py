from numpy import empty
from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move import Coordinate, Move
from copy import deepcopy

'''
        _
    .__(.)<   (MEOW)
     \___)
~~~~~~~~~~~~~~~~~~~~~~~~~
'''
def _astar_heuristic(cur: State, _goal):
    if 0:
        m = _goal[0] - cur.current_pos.x
        n = _goal[1] - cur.current_pos.y

        if m % 2 == 0:
            cur.h = 2**n - m * (2**n - 8) / 2
        else:
            cur.h = (((((2*(m-1)/2))*(2**(n-1))+2*(m+1)/2))/(2**(n-1)))-((m-1)/2-1)*2*2 - (((m-1)/2)+1)*2*(2**(n-1)) + 2*m 
        return cur.h

    return 0

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
    _open = list()
    _open.append(start)

    # closed nodes
    _closed = []

    # goal node
    _goal = start.board_size

    # Save state for good path
    _min_cost = 1
    _min_path = State()

    # run A* until break;
    while _open:
        # get node with minimum f
        _f_node_open = [node.f for node in _open]
        _min_f = min(_f_node_open)

        # pop the node with min f for expansion
        _current = deepcopy(_open.pop(_f_node_open.index(_min_f)))

        # add that node to _closed
        _closed.append(_current)

        # stop if popped goal node
        if _current.current_pos == Coordinate(*_goal):
            if _current.current_tax <= 0:
                print("ping! ->", _current.current_tax)
                if _current.current_tax < _min_cost:
                    print("found better path")
                    _min_cost = _current.current_tax
                    _min_path = deepcopy(_current)
                    print("tax:", _min_cost)
                    if _min_cost < -2: break

                continue
    
        # get available moves, continue if none is found
        if _current.available_moves_list() is empty:
            continue

        for _move in _current.available_moves_list():
            # temporary node
            temp = deepcopy(_current)
            
            # current tax as g
            temp.g = temp.tax_after_move(_move) #NO need to convert to current_tax later

            # heuristic func as h
            #--> blame Nam for weird heuristic
            temp.h = _astar_heuristic(
                temp,
                _goal
            )
            #DEBUG: all movable tiles
            #print("at:", _current.current_pos, ", move:", _move)

            # A* function
            temp.f = temp.g + temp.h

            # check if node w/ better A* function f is available in _open
            t_do_continue = False
            for t_node in _open:
                if t_node.f < temp.f:
                    t_do_continue = True
                    break

            # ignore temp and expand this t_node instead
            #if t_do_continue:
            #    continue

    
            # temp has great f, so add that to _open.
            # and move it
            temp.move_on_move(_move)

            # attach parent node & moved dir to temp
            #-- like a linked list, hrmf..
            temp.parent = _current
            temp._move = _move

            # that TODO up there-----------------------^
            #print("move to", temp.current_pos, "tax:", temp.current_tax)

            # finally, add it to _open
            _open.append(temp)

        
    path = []
    while _min_path.parent is not None:
        path.append(_min_path._move)
        _min_path = _min_path.parent

    return path[::-1]    

if __name__ == "__main__":
    _internalVar = State()
    _internalVar.initialize_4x4_default()
    print(*astar(_internalVar), sep = '\n')