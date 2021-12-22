from typing import List
from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move import Coordinate, Move
from AI_intro_project._Utilities import _Utilities
from copy import deepcopy
import time
MODE_DBG = False

'''
	
                        /|/|/|\\|\|                                       
                      |  | | | | | |\                                   
                    | | |  | || || | |\                                  
                   /  | | |  || || ||||                                
                   || | | |  | | |  | |\                                
                 |  | | |  || ||  | | | \                                
                /  |  | |  ||  | || | ||\                               
                | | | | | || |  ||   | | |                              
                | | |    | | || |  | | |||\                             
               || |  | | | |  | || | | ||| \                           
              ||  |    |   | | ||| |     | |                            
              ||| | | |  | | |  || | | ||  |\                           
              | | | | |  |   | || |||| ||| |\                           
             /|  |  | | |  |  | | | || | ||  |                            
             |||| | |__ |__| |__|   || | || ||\                         
            |_| _ --,   ,.. ,   ,.... _|_|_ || |\                       
            /,   ,..,    ,.,    ,.. ,   ,..-|_\| |                       
         _ /.,    ,.,    ,,     ,...   ,...,   .\\                        
      _ /  ,..,    ,     ,      ,.,    ,.,    _ ...\\\\                 
    _/       ',,   ,     ,       ,     .       \  .   .\\\\             
  /     .       _--                       -\    \  .   ..  \\\\\           
 /    O .   __ /    _/                 ____|    \       .       \\\\\\\  
 /      |---  /    /---__________------    |    |---____            |  \  
/    ,; /     |    |                       |nn  |       ---____     |  |  
|,,,','/      /nn  |                                            ---|   |   
 ;,,;/                                                     _______/   /   
                                                   --------_________/                                                        
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


#################################################
# DFS magics
def dfs(cur):
    # ABORT: out of time
    global t_limit_r
    if t_limit_r: pass
    elif time.time() - t_start > t_limit:
        print(f"ABORT: time limit reached: {t_limit}", file = f)
        t_limit_r = True
        pass

    else:
        # ABORT signal var
        global exiting
        if not exiting and cur.available_moves_list() is not None:
            for _move in cur.available_moves_list():
                # ABORT signal
                if exiting: break

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
                    
                    GOAL.path = temp.path

                _c = _move.coordinate_end_calc()
                _move = Move(
                    _c.x,
                    _c.y,
                    _move.reverse_direction()
                )
                temp.path.append(_move)

                dfs(temp)    

if __name__ == "__main__":
    t_limit = 30 # seconds

    with open("AI_intro_project/search_algo/load_all_output/output-dfs.txt", "w") as f:
        for _internalVar in _Utilities().load_all(
            sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
            directory='AI_intro_project/randomized_states',
            extension='state'
        ):
            timer = time.time()

            # print basic info
            print("\nboard size:",_internalVar.board_size, file = f)
            print(
                f"start at: ({_internalVar.current_pos.x}, {_internalVar.current_pos.y})",
                file = f
            )
            print("tax:", _internalVar.current_tax, file = f)

            # signal DFS to ABORT: found solution
            exiting = False

            # time limit
            t_start = time.time()
            t_limit_r = False

            # print
            print(*dfs_prep(_internalVar), sep = '\n', file = f)

            timer -= time.time()
            print(f"time: {-timer}", file = f)