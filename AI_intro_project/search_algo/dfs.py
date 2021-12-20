from typing import List
from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move import Coordinate, Move
from copy import deepcopy
import time
MODE_DBG = False

'''
        _
    .__(.)<   (MEOW)
     \___)
~~~~~~~~~~~~~~~~~~~~~~~~~                                                        
'''
def dfs_prep(START: State):
    ''' init basic vars '''
    #############################################
    # Auxiliary vars for reduced querying need
    global _START_point, _board_size, _START_tax, GOAL


    _board_size = START.board_size
    _START_point = START.current_pos
    _START_tax = START.current_tax

    #############################################
    # GOAL: where we start our path-finding:
    #       inherit properties from START.
    GOAL = deepcopy(START)
    GOAL.current_pos = Coordinate(*GOAL.board_size)
    GOAL.current_tax = 0
    GOAL.walked_moves = START.walked_moves
    print("GOAL:", GOAL.current_pos, ',', GOAL.current_tax)

    # attach a visited list
    GOAL.path = list()

    #############################################
    # START: where we are ending
    #DBG!: print its stats
    print("START:", _START_point, ',', _START_tax)

    
    dfs(GOAL)
    return GOAL.path[::-1]

def dfs(cur):
    global exiting
    if not exiting and cur.available_moves_list() is not None:        
        #DBG!: move where?
        for _move in cur.available_moves_list():
            print(_move)
            # temporary node
            temp = deepcopy(cur)

            # and move to that node
            temp.move_on_move(_move)
            if cur.current_pos == _START_point:
                # found path
                if cur.current_tax >= _START_tax:
                    # found solution
                    GOAL.path = temp.path
                    exiting = True
                    break

            _c = _move.coordinate_end_calc()
            _move = Move(
                _c.x,
                _c.y,
                _move.reverse_direction()
            )
            temp.path.append(_move)

            dfs(temp)    

if __name__ == "__main__":
    timer = time.time()

    # init
    _internalVar = State()
    _internalVar.initialize_6x6_default()
    global exiting
    exiting = False

    # print
    # note: astar has another argument: OBJECTIVE = one_of("OPTIMAL", "MORALITY")
    print(*dfs_prep(_internalVar), sep = '\n')

    timer -= time.time()
    print(f"time: {-timer}")