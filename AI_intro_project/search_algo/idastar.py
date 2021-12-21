from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move import Coordinate, Move
from AI_intro_project._Utilities import _Utilities
from copy import deepcopy
import time
MODE_DBG = False

'''
@@@@@@@@@@@@@@@@@@@@@**^^""~~~"^@@^*@*@@**@@@@@@@@@
@@@@@@@@@@@@@*^^'"~   , - ' '; ,@@b. '  -e@@@@@@@@@
@@@@@@@@*^"~      . '     . ' ,@@@@(  e@*@@@@@@@@@@
@@@@@^~         .       .   ' @@@@@@, ~^@@@@@@@@@@@
@@@~ ,e**@@*e,  ,e**e, .    ' '@@@@@@e,  "*@@@@@'^@
@',e@@@@@@@@@@ e@@@@@@       ' '*@@@@@@    @@@'   0
@@@@@@@@@@@@@@@@@@@@@',e,     ;  ~^*^'    ;^~   ' 0
@@@@@@@@@@@@@@@^""^@@e@@@   .'           ,'   .'  @
@@@@@@@@@@@@@@'    '@@@@@ '         ,  ,e'  .    ;@
@@@@@@@@@@@@@' ,&&,  ^@*'     ,  .  i^"@e, ,e@e  @@
@@@@@@@@@@@@' ,@@@@,          ;  ,& !,,@@@e@@@@ e@@
@@@@@,~*@@*' ,@@@@@@e,   ',   e^~^@,   ~'@@@@@@,@@@
@@@@@@, ~" ,e@@@@@@@@@*e*@*  ,@e  @@""@e,,@@@@@@@@@
@@@@@@@@ee@@@@@@@@@@@@@@@" ,e@' ,e@' e@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@" ,@" ,e@@e,,@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@~ ,@@@,,0@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@,,@@@@@@@@@@@@@@@@@@@@@@@@@                                                     
'''
##########################
#   [ SUMMARY ]
# Starting point: GOAL, with cost = 0
# Objective: find path to Start, with:
#   > FEASIBLE: Cost at START-point is the same as, or slightly higher.
#               (which corresponds to that cost at GOAL is approaching 0)
# How:
#   > Start from GOAL node. Find path to START node with either obj above.
#   > A*: f_limit >= f = g + h, where:
#       f: A* function.
#       g: cost accumulated at current node.
#       h(FEASIBLE): a function that heavily bias the biggest outer-loop possible
#          --> aim: speed up finding possible path
#          --> char: + still struggles with big board where it should be quick to find.
#                    + takes MUCH longer than OPTIMAL (or Dijkstra) and as
#                      much space for NOT_FOUND scenario.
#                    + is not very space efficient, considering this is 
#                      pretty much cheating the way thru.
#       f_limit: Start at 8, iterate by 8.
#
#     NOTE: IDA* does not support OPTIMAL mode.
#
###################################
'     !FYI: IT IS VERY SLOW.'
'           YOU HAVE BEEN WARNED'



'''
heuristic variables:

cur:       current node
mid_point: self-explanatory
x, y:      Coordinate of START (for Manhattan distance)
b:         a binary variable to detect that cost is changing sign
'''
def _astar_heuristic(cur, mid_point, x, y, b):

    # manhattan of current node
    mht_to_midpoint = abs(cur.current_pos.x - mid_point[0]) + abs(cur.current_pos.y - mid_point[1])
    mht_to_START = abs(cur.current_pos.x - x) + abs(cur.current_pos.y - y)

    # inflated/highly-biased heuristic
    #   yes, this heuristic function is definitely NOT admissible
    #   it cannot be anyways, in this problem
    if cur.current_pos.x == 0 and cur.current_pos.y == 1:
        b = 1

    #h = 2 * (- mht_to_midpoint - mht_to_START + mht_start_to_midpoint)
    if b == 0:
        h = 2 * ((mid_point[0]*2 - cur.current_pos.x) * 4 + mid_point[1]*2 - cur.current_pos.y)  
        #   ^ random    ^ board_size[0]                           ^ board_size[1]
        # heavily favors all-L, then all-U
    else:
        h = 8 * (mid_point[0] * mid_point[1] *4 - abs(x - cur.current_pos.x) - abs(y - cur.current_pos.y))
        #   ^ random   ^ bsize[0]  *  ^ bsize[1]      | START.x - cur.x |            | START.y - cur.y |
        # heavily favors going as quick as possible to START

    return h

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
def astar(START):

    ''' init basic vars '''
    #############################################
    # Auxiliary vars for reduced querying need

    _board_size = START.board_size
    _mid_point = (_board_size[0]/2, _board_size[1]/2)
    _START_point = START.current_pos
    _START_tax = START.current_tax
    _max_path = None

    #############################################
    # GOAL: where we start our path-finding:
    #       inherit properties from START.
    GOAL = deepcopy(START)
    GOAL.current_pos = Coordinate(*GOAL.board_size)
    GOAL.current_tax = 0
    GOAL.walked_moves = START.walked_moves
    #print("GOAL:", GOAL.current_pos, ',', GOAL.current_tax, file = filename)

    # starting with f = 0 and b = 0
    #-- Doesn't matter if is calculated properly.
    GOAL.f = 0
    GOAL.b = 0

    # attach a parent node
    #-- Linked List intensifies_
    GOAL.parent = None

    #############################################
    # START: where we are finding path to
    #DBG!: print its stats
    #print("START:", _START_point, ',', _START_tax)

    #############################################
    # variables supporting A* function

    # _open: list of node(s) we want to expand
    _open = list()
    _open.append(GOAL)

    # _max_cost/OPTIMAL only: the highest possible COST found, following objective 
    _max_cost = _START_tax

    # _moral_cost/FEASIBLE only: reduce querying START.current_tax
    _moral_cost = _START_tax

    # IDA* exclusive: 
    # f limiting
    f_limit = 8

    # path checking: 
    #   ABORT immediately if f_limit > max(all_of f)
    #   and no path was found
    f_max = 0
    
    ''' run IDA* until f_limit reached '''
    # path is not found yet, increment f_limit
    while _max_path is None:
        print(f_limit)
        # there is node in _open
        while _open:
            ##################################################
            # [ pick & pop node with highest node.f for expansion ]

            # craft list of node's f (A* function)
            _f_node_in_open = [node.f for node in _open]

            # find one with minimum f
            _max_f_node_in_open = max(_f_node_in_open)

            # pop the node with minimum f for expansion
            _current = deepcopy(_open.pop(_f_node_in_open.index(_max_f_node_in_open)))

            #?!: add that node to _closed
            #_closed.add(_current)
            
            # stop if popped START node --> we found a path to it
            if _current.current_pos == _START_point:
                # FEASIBLE: tax must be the same as,
                # or slightly bigger than START tax. 
                # If found, break immediately.
                if _current.current_tax >= _moral_cost:
                    print("found path!")

                    # borrow _max_path for easier print
                    _max_path = _current
                    break

            # get available moves, skip this node if none is found
            if _current.available_moves_list() is None:
                continue

            ###############################################
            # [ Promising node, move there and calculate node.f ]
            for _move in _current.available_moves_list():
                #DBG!: move where?
                #if _move == Move(1, 0, 'R'):
                #    print("poking:", _move)

                # temporary node
                temp = deepcopy(_current)
        
                # and move to that node
                temp.move_on_move(_move)
        
                if temp.available_moves_list() is None: continue

                #DBG!: data:
                #print(f"at {temp.current_pos} after {_move}: tax = {temp.current_tax}")
                
                # attach parent node to temp
                #-- like a linked list, hrmf...
                temp.parent = _current
            
                # g: if-moved current_tax as g
                temp.g = temp.tax_after_move(_move) 

                # h: heuristic function, explanation above
                temp.h = _astar_heuristic(
                    temp,
                    _mid_point,
                    _START_point.x,
                    _START_point.y,
                    temp.b
                )

                # f: A* function
                temp.f = temp.g + temp.h

                # save ABORT condition f_max
                if temp.f > f_max: f_max = temp.f

                # STOP exploring if exceeding f_limit
                if temp.f > f_limit:
                    continue

                # attach moved dir to temp, will need for printing later.
                # reverse because we are finding from GOAL to START.
                _c = _move.coordinate_end_calc()

                temp._move = Move(
                    _c.x,
                    _c.y,
                    _move.reverse_direction()
                )
                # this node _might_ lead to optimal path .
                # so, append it to _open.
                _open.append(temp)

        #################################################
        # while: f_limit reached, open empty, but no path found.

        # ABORT: not found solution in regular A*.
        #   oh sweet sweet Alabama the wait.
        if f_limit > f_max: break

        # re-run the whole thing,
        # iterate by +8
        _open.append(GOAL)
        f_limit += 8

    # return-inator
    path = []
    try:
        while _max_path.parent is not None:
            path.append(_max_path._move)
            _max_path = _max_path.parent

        return path

    except NameError:
        return ["NOT FOUND!"]


if __name__ == "__main__":
    if 0:
        with open("AI_intro_project/search_algo/load_all_output/output.txt", "w") as f:
            # init
            for _internalVar in _Utilities().load_all(
                sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
                directory='AI_intro_project/randomized_states',
                extension='state'
            ): pass

    else:
        _internalVar = State()
        _internalVar.initialize_4x4_default

    timer = time.time()

    # print basic info
    print("board size:",_internalVar.board_size)
    print(
        f"start at: {_internalVar.current_pos.x}, {_internalVar.current_pos.y}"
    )
    print("tax:", _internalVar.current_tax)
    # note: astar has another argument: OBJECTIVE = one_of("OPTIMAL", "FEASIBLE")
    print(*astar(_internalVar, OBJECTIVE = "FEASIBLE"), sep = '\n')

    timer -= time.time()
    print(f"time: {-timer}")