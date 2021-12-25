from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move import Coordinate, Move
from AI_intro_project._Utilities import _Utilities
from copy import deepcopy
import time, psutil
import matplotlib.pyplot as plt

MODE_DBG = False
if MODE_DBG: print("===\n!DBG: Debug Mode is on\n===")
def get_ram_usage(): return int(psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024**3)

'''
   .-=-.
 _/     `.
/_( 9    |.__
  \          ``-._
   `>    _...     `'>
    |  .'    `-. _,'
     \ `-.    ,' ;
      `.  `~~'  /
      _ 7`"..."'
      ,'| __/
          ,'\                                                      
'''
##########################
#   [ SUMMARY ]
# Starting point: GOAL, with cost = 0
#
# Objective: find path to START with cost >= START.current_tax
#
# About DFS:
#  > expanding "node" in order of L <-; U ^ ; R ->; D v
#  > fully ensure DFS will form a (big) counter-clockwise loop when moving from START to GOAL,
#    thus quickly and effortlessly "cheating tax".
#  > Strength/Weakness:
#    +> If possible, DFS can find path EXTREMELY quickly, albeit a few exceptions in Weakness.
#       > Limiting time to either 10 or 60 seconds yields no difference in solved/unsolved states.
#    +> is very space friendly. Of all 28 solved states, only 2 exceeded 100 recursive iterations.
#
#    -> Cannot find path if there can only be a way into/out-of START node (len(START.available_moves_list()) <= 1)
#       (under time limit and/or space/recursion limit; this does not count move-to-(0,0))
#       > This weakness is very clear in 21/50 unsolved states, where each run iterates no less than 5000 times.
#       > 1 state is unsolvable in all 3 algorithms we implemented and by brute-force, so it is excluded.
#
##########################

def dfs_prep(START):
    ''' init basic vars '''
    #############################################
    # Auxiliary vars for reduced querying need
    #DBG!: number of recursive DFS iterations
    global _START_point, _board_size, _START_tax, GOAL, __t, ite
    ite = 0
    
    __t = -1
    _board_size = START.board_size
    _START_point = START.current_pos
    _START_tax = START.current_tax

    #############################################
    # GOAL: where we start our path-finding:
    #       inherit properties from START.
    GOAL = deepcopy(START)
    GOAL.current_pos = Coordinate(*_board_size)
    GOAL.current_tax = 0

    #DBG!: info
    if MODE_DBG: print("GOAL:", GOAL.current_pos, ',', GOAL.current_tax)

    # attach a visited list
    GOAL.path = list()

    #############################################
    # START: where we are ending
    #DBG!: info
    if MODE_DBG: print("START:", _START_point, ',', _START_tax)

    dfs(GOAL)
    #DBG!: ite, explained above
    if MODE_DBG: print(ite)
    
    return GOAL.path[::-1]


#################################################
# DFS magics
def dfs(cur):
    # ABORT: out of time
    global t_limit_r, __t
    if t_limit_r: pass
    elif time.time() - t_start > t_limit:
        print(f"ABORT: time limit reached: {t_limit}", file = f)
        t_limit_r = 1
        pass
    else:
        # ABORT: exiting
        global exiting, ite
        if not exiting and cur.available_moves_list() is not None:
            for _move in cur.available_moves_list():
                #DBG!: iter
                ite += 1

                if exiting: break

                # temporary node
                temp = deepcopy(cur)

                # and move to that node
                temp.move_on_move(_move)
                
                _c = _move.coordinate_end_calc()
                _mv = Move(
                    _c.x,
                    _c.y,
                    _move.reverse_direction()
                )
                temp.path.append(_mv)
                
                if temp.current_pos == _START_point:
                    # found path
                    if temp.current_tax >= _START_tax:
                        # found solution
                        GOAL.path = temp.path
                        __t = temp.current_tax
                        exiting = True
                        break
                    
                    GOAL.path = deepcopy(temp.path)
                    
                    # Prevent loss of possible solution
                    if len(temp.available_moves_list()) <= 1: continue
                
                dfs(temp)    

if __name__ == "__main__":
    t_limit = 10 # seconds
    t_all = 0
    t_ite = 0

    # Figure of (un-)solved paths
    path = 'AI_intro_project/_s_dfs_solved_state_images/'
    
    #CSV!: open CSV file
    with open("AI_intro_project/search_algo/load_all_output/output-dfs.csv", "w") as f_csv:
        print('idx,path_length,tax,time,time_limit_reached,iteration,ram_usage', file = f_csv)
    
        with open(f"AI_intro_project/search_algo/load_all_output/output-dfs-L{t_limit}.txt", "w") as f:
            _var_utils_loadall = _Utilities().load_all(
                sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
                directory='AI_intro_project/randomized_states',
                extension='state'
            )

            for idx, _internalVar in enumerate(_var_utils_loadall):
                # start timer
                timer = time.time()

                # print basic info to output file
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
                t_limit_r = 0

                # print
                print(*(moves:=dfs_prep(_internalVar)), sep = '\n', file = f)
                if t_limit_r: print(f"reached time limit: {t_limit}", file = f) 
                for mv in moves:
                    _internalVar.move_on_move(mv)
                
                #_internalVar.visualize()
                _internalVar._plt_prepare()
                plt.savefig(path + str(idx).zfill(2))
                plt.clf()
                
                timer -= time.time()
                print(f"time: {-timer}", file = f)

                if abs(timer + t_limit) >= 2: t_all -= timer
                t_ite += ite
                ###############
                #CSV!
                # in order: boardSize(m, n), #OfMoves, finalTax, isTimeLimitReached?
                print(f'{idx},{len(moves)},{-__t},{-timer},{t_limit_r},{ite},{get_ram_usage()}', \
                    file = f_csv)
        print(t_all, t_ite)