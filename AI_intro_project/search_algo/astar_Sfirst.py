#!/usr/bin/python3
import matplotlib.pyplot as plt
from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move import Coordinate, Move
from AI_intro_project._Utilities import _Utilities
from copy import deepcopy
from functools import reduce
import time

# GLOBAL DEBUG MODE: print debug info of algorithm
MODE_DBG = True
if MODE_DBG: print("===\n!DBG: Debug Mode is on\n===")

'''
                MEOW

  /\ ___ /\ 
 (  o   o  )
  \  >#<  /
  /       \ 
 /         \       ^
|           |     //
 \         /    //
  ///  ///   --
'''

##########################
#   [ SUMMARY ]
# Starting point: START, with cost = START.current_tax
#
# Objective: find path to GOAL, with either mode:
#   > OPTIMAL: Cost at GOAL-point is LOWEST possible.
#   > FEASIBLE: Cost at GOAL-point is NO HIGHER than 0.
#
# How:
#   > Start from START node. Find path to GOAL node with either obj above.
#
#   > A*: f = g + h, where:
#       f: A* function.
#       g: cost accumulated at current node.
#
#       @[ABANDONED; REASON: too slow and space-inefficient]
#       h(OPTIMAL): Manhattan distance from Node to the "middle" of the board.
#          --> aim: favors path that distances itself from the middle point.
#          ? > why: a counter-clockwise loop is the only way to "cheat" tax.
#          --> char: + is very slow and space-inefficient (need to expand most nodes).
#               ^    + should find the actual optimal, or slightly suboptimal 
#               |      path quickly, however the algo does not know it.
#               |      -> by brute-forcing, OPTIMAL is a path that covers most of
#               |         the board (usually leaving 1 node) and loops counter-clockwise 
#               |         from inside out.
#               |
#               | <--- Due to cost wildly fluctuating (by rule),
#               | <--> cannot calculate/prove the minimum (OPTIMAL) cost mathematically.
#                      (example: 4x4, (0,2): -4 || 6x6, (0,3): -248 || 8x8, (0,4): -2012
#
#          --> illustration of OPTIMAL on 4x4:
#
#            ------> S   D   L
#            D   L  D/L  L   U   
#            D   D   L   .   U 
#            D   R   R   R   U
#            R   R   R   R   G
#
#       @[DEFAULT]
#       h(FEASIBLE): a function that prioritizes making counter-clockwise loop(s)
#          --> aim: speed up finding possible path(s)
#          --> char: + struggle with START point (x, y), where both x and y is no 
#                      smaller than 1. However searching path for big board is
#                      fairly quickly (< 30sec/board, if found).
#                    + fairly efficient space-wise, iterating less than 2000 times
#                      for all boards with found path and slightly over for unsolved 
#                      boards (under time limit 60).
#                    + Solved 47/50 boards with time limit 60 seconds.
#                    --- 
#                    + disregarded admissibility/consistency: 
#                      impossible that 0 <= h(N) <= h'(N) if h'(N) <= 0
# 
##########################
'''
FEASIBLE heuristic 

variables:
    cur            || current node
    cur_x, cur_y   || Coordinate of current node
    mid_point      || (of the board)
'''
def _astar_heuristic_FEASIBLE(cur, mid_point):
    cur_x = cur.current_pos.x
    cur_y = cur.current_pos.y

    # board = (m, n)
    # formula = n/2 * y * (n - y) + x
    # _insert "but why" meme here_
    h = mid_point[1] * cur_y * (mid_point[1]*2 - cur_y) + cur_x
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
def astar(START, ofile, OBJECTIVE = 'FEASIBLE'):
    ''' init basic vars '''
    #############################################
    # Auxiliary vars

    _board_size = START.board_size
    _mid_point = (_board_size[0]/2, _board_size[1]/2)
    _START_point = START.current_pos
    _START_tax = START.current_tax
    _min_path = None
    t_limit_r = False
    
    #DBG!: counting iterations
    if MODE_DBG: ite = 0

    #############################################
    # GOAL: where we end our path-finding:
    #       inherit properties from START.
    GOAL = deepcopy(START)
    GOAL.current_pos = Coordinate(*GOAL.board_size)

    #DBG!: print GOAL info
    if MODE_DBG: print("GOAL:", GOAL.current_pos)


    #############################################
    # START: where we are finding path to
    #DBG!: print its stats
    if MODE_DBG: print("START:", _START_point, ',', _START_tax)

    # attach a parent node
    #-- Linked List intensifies_
    START.parent = None

    # first f
    START.f = 0

    # [REGRESSED]
    # OBJECTIVE: set objective:
    #   > OPTIMAL
    #   > FEASIBLE
    # (set it in main)
    if OBJECTIVE not in ['FEASIBLE', 'OPTIMAL']:
        print('ABORT: please check OBJECTIVE typo')
        pass
    
    _OBJECTIVE = OBJECTIVE

    #############################################
    # variables supporting A* function
    # _open: list of node(s) we want to expand
    _open = list()
    _open.append(START)

    # list that save taxes of found-but-unsastified paths
    _all_path_tax = list()


    ''' run A* until break, expanding all nodes '''
    while _open:
        # ABORT: out of time
        if time.time() - t_start > t_limit: 
            print(f"reached time limit: {t_limit}", file = ofile)
            if MODE_DBG: print(f"reached time limit: {t_limit}")
            t_limit_r = True
            break

        ##################################################
        # [ pick & pop node with lowest node.f for expansion ]

        # craft list of node's f (A* function)
        _f_node_in_open = [node.f for node in _open]

        # find one with minimum f
        _min_f_node_in_open = min(_f_node_in_open)

        # pop the node with minimum f for expansion
        _current = deepcopy(_open.pop(_f_node_in_open.index(_min_f_node_in_open)))

        # stop if popped GOAL node --> we found a path to it
        if _current.current_pos == GOAL.current_pos:            
            if _OBJECTIVE == "FEASIBLE":
                # FEASIBLE: tax must be the same as,
                # or slightly bigger than START tax. 
                # If found, break immediately.
                if _current.current_tax <= 0:
                    if MODE_DBG: print("found path!")

                    # borrow _min_path for easier print
                    _min_path = _current
                    break
                
                # if not sastified, save the best path we've found
                # it helped in the making of that weird heuristic
                # owo~
                _last_cost = _current.current_tax
                _all_path_tax.append(_last_cost)
                if _last_cost == min(_all_path_tax):
                    _last_path = deepcopy(_current)


        # get available moves, skip this node if none is found
        _moves = _current.available_moves_list()
        if _moves is None:
            continue

        ###############################################
        # [ Promising node, move there and calculate node.f ]
        for _move in _moves:
            #DBG!: iteration counter
            if MODE_DBG: ite += 1

            #DBG!: move where?
            # print("poking:", _move)

            # temporary node
            temp = deepcopy(_current)
    
            # and move to that node
            temp.move_on_move(_move)
            temp.g = temp.current_tax
            #print(temp.g)
            
            if temp.available_moves_list() is None: continue

            #DBG!: data:
            #print(f"at {temp.current_pos} after {_move}: tax = {temp.current_tax}")
            
            # attach parent node to temp
            #-- like a linked list, hrmf...
            temp.parent = _current

            # h: heuristic function, explanation above
            h_func = "_astar_heuristic_" + OBJECTIVE
            temp.h = globals()[h_func](
                temp,
                _mid_point
            )

            # f: A* function
            temp.f = temp.g + temp.h

            #DBG!: info of A*
            # if MODE_DBG: print(temp, ':', temp.f, '=', temp.g, '+', temp.h)
            
            # attach moved dir to temp, will need for printing later.
            temp._move = _move

            # this node _might_ lead to a FEASIBLE path.
            # so, append it to _open.
            _open.append(temp)

    try:
        # has the time limit reached?
        # if yes, get the last path A* found
        if t_limit_r: _min_path = _last_path

        # using "linked" node to find path
        path = []
        while _min_path.parent is not None:
            path.append(_min_path._move)
            _min_path = _min_path.parent

        #DBG!: print iteration counter
        if MODE_DBG: print(_board_size, ite)
        return path[::-1]

    except:
        # time limit reached, but A* didn't find any path
        # return nothing ~> visualize nothing
        return []

if __name__ == "__main__":
    # TIME LIMIT
    t_limit = 60

    # Figure of (un-)solved paths
    path = 'AI_intro_project/_s_astar-Sf_solved_state_images/'

    # _Utils.load_all()
    with open("AI_intro_project/search_algo/load_all_output/output-astar.txt", "w") as f:
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
            
            # A*, return list()
            #-- start timer
            t_start = time.time()
            print(*(moves:=astar(_internalVar, ofile = f, OBJECTIVE="FEASIBLE")), sep='\n', file=f)

            # save figure at $path
            for move in moves:
                _internalVar.move_on_move(move)
            
            #_internalVar.visualize()
            _internalVar._plt_prepare()
            plt.savefig(path + str(idx).zfill(2))
            plt.clf()
            
            # end counter and print
            timer -= time.time()
            print(f"time: {-timer}", file = f)

# c
#   a     >owo<
#     t
# 3 number 3s. Ayyy