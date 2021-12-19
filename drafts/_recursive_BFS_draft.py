
from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move \
                import Coordinate, Move

from heapq import nsmallest,heappop, heapify
import math


class Node:
   def __init__(self, origin: Move, g = 0, parent = None):
    #Move tạo ra Node
    self.origin = origin

    #Past_cost
    self.g = g

    #Node mục tiêu
    self.goal = goal

    #giá trị heuristic
    self.h = 0

    #giá trị hàm đánh giá( f= g+h)
    self.f = 0

    #độ sâu của node
    self.depth = 0

    # node cha
    self.parent = parent
    if parent:
        self.depth = parent.depth + 1


   def __repr__(self):
    return 'Node'+str((self.origin.coordinate_end.x,self.origin.coordinate_end.y))

   def __lt__(self,other):
    return self.origin.coordinate_end.x > other.origin.coordinate_end.x

   def __eq__(self,other):
    if self.__class__ == other.__class__:
        return self.origin.coordinate_end == other.origin.coordinate_end

   def child_node_list(self,state: State):
        '''danh sách node con'''
        return [Node(child,parent = self) for child in state.available_moves_list()]


   def heuristic(self):
    '''hàm heuristic'''
    if self.origin.direction == 'L':
        #ưu tiên đi lên(/2) -> trái(-2) -> xuống(+2)
        self.h = self.child_node_list
    elif self.origin.direction == 'R':
        #ưu tiên đi xuống
        self.g = self.parent.g + 2
    elif self.origin.direction == 'U':
        #ưu tiên sang trái
        self.g = self.parent.g /2
    elif self.origin.direction == 'D':
        #ưu tiên sang phải
        self.g = self.parent.g * 2
    self.h = 0
    return self.h

   def pathway(self):
    '''lưu lại quãng đường đã đi'''
    node = self
    path = []
    while node:
        path.append(node.origin)
        node = node.parent
    return list(reversed(path))[1:]

   def past_cost(self):
        '''chi phí đã đi của node'''
        if self.origin.direction == 'L':
            self.g = self.parent.g - 2
        elif self.origin.direction == 'R':
            self.g = self.parent.g + 2
        elif self.origin.direction == 'U':
            self.g = self.parent.g /2
        elif self.origin.direction == 'D':
            self.g = self.parent.g * 2
        return self.g



def RBFS(state: State, startnode: Node, goalnode: Node, f_limit: float):
   '''thuật toán trả lại 2 giá trị là [node , f_limit mới]'''
   print("\nIn RBFS Function with node ", startnode, " with node's f value = ", startnode.f , " and f-limit = ", f_limit)

   #điều kiện dừng của recursive
   if startnode == goalnode and startnode.g <= 0:
    return[startnode, None]

   #list lưu lại khi expand 1 node
   successors = []
   for child in startnode.child_node_list(state):
    if child.origin in startnode.pathway():
        continue
    else:
        child.g = child.past_cost()
        child.f = max(child.g + child.heuristic(),startnode.f)
        successors.append((child.f,child))

   print('The next node to move can be', successors)

   # điều kiện nếu node ko còn đường nào để đi
   if len(successors) <= 0:
    return [None, math.inf]

   #vòng recursive, chọn node có f nhỏ nhất trong node con, nếu node.f mới lớn hơn f_limit, cập nhật f_limit
   while True:

      if len(successors) == 0:
        return [None, math.inf]
      heapify(successors)
      nextNode = heappop(successors)
      state.current_pos = nextNode[1].origin.coordinate_end
      if nextNode[1].f > f_limit:
        return [None, nextNode[1].f]
      if len(successors) != 0:
        alternative = nsmallest(1, successors)[0][0]
      else:
        alternative = math.inf

      [result,nextNode[1].f] = RBFS(state, nextNode[1], goalnode, min(f_limit, alternative))

      if result != None:
        return [result, None]


if __name__ == '__main__':

    s = State()
    s.initialize_8x8_default()

    startnode = Node(s.walked_moves[-1], s.current_tax)

    #goalnode = Node(Move(s.board_size[0], s.board_size[1]-1, 'R') , 0)
    goalnode = Node(Move(s.board_size[0]-1, s.board_size[1], 'D'), 0)

    solution = RBFS(s, startnode, goalnode, math.inf)
    if solution[0] != None:
        for k in solution[0].pathway():
            s.walked_moves.append(k)
        s.current_tax = solution[0].g
    else:
        raise RuntimeError
    s.visualize()

