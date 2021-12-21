from AI_intro_project.State import State
from AI_intro_project.Coordinate_and_Move \
                import Coordinate, Move

from heapq import nsmallest,heappop, heapify
import math
from AI_intro_project._Utilities import _Utilities


class Node:
   def __init__(self, origin: Move, g = 0, parent = None):
    #Move tạo ra Node
    self.origin = origin

    #Past_cost
    self.g = g

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
        return [Node(child, parent = self) for child in state.available_moves_list()]


   def heuristic(self,state: State):
    '''hàm heuristic'''
    #h =  g *( distance from node to goal)  (idol nào cứu giúp e)
    self.h = self.g*((abs(self.origin.coordinate_end.x - state.board_size[0]) + abs(self.origin.coordinate_end.y -state.board_size[1])))
    #phần này e ko bt làm ntn
    #m = state.board_size[0] - self.origin.coordinate_end.x
    #n = state.board_size[1] - self.origin.coordinate_end.y
    #if m % 2 == 0:
        #self.h = ((((((2*(m/2))*(2**(n-1))+2*(m/2))/(2**(n-1)))-((m/2)-1)*2)*2 - ((m/2)+1)*2)*(2**(n-1))) + 2*m
    #else:
        #self.h = ((((((2*((m-1)/2))*(2**(n-1))+2*((m+1)/2))/(2**(n-1)))-(((m-1)/2)-1)*2)*2 - (((m-1)/2)+1)*2)*(2**(n-1))) + 2*m
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



def RBFS(state: State, node: Node, goalnode: Node, f_limit: float):
   '''thuật toán trả lại 2 giá trị là [node , f_limit mới]'''
   print("\nIn RBFS Function with node ", node, " with node's f value = ", node.f , " and f-limit = ", f_limit)
   global z, m
   m += 1
   #điều kiện dừng của recursive
   if node == goalnode:
    z.append((node.g, node))

    if node.g <= 0:
        return[node, None]
    else:
        return[None, math.inf]

   if m >= 100000:
    if len(z) != 0:
        return[min(z)[1], None]
    else:
        print('Các idol cứu em với, nó ko duyệt qua được hết tất cả các trường hợp ý')
        return [Node(Move(0,0,'None')) ,None]


   #list lưu lại khi expand 1 node
   successors = []
   for child in node.child_node_list(state):
    if child.origin in node.pathway():
        continue
    else:
        child.g = child.past_cost()
        child.f = max(child.g*len(child.pathway()) + child.heuristic(state),node.f)
        successors.append((child.f,child))

   print('The next node to move can be', successors)

   # điều kiện nếu node ko còn đường nào để đi
   if len(successors) == 0:
    return [None, math.inf]

   #có vẻ phần vòng lặp này sai nhg tui ko bt sửa ntnao
   #vòng recursive, chọn node có f nhỏ nhất trong node con, nếu node.f mới lớn hơn f_limit, cập nhật f_limit
   while True:
      if len(successors) == 0:
        return [None, math.inf]
      heapify(successors)
      best = heappop(successors)
      state.current_pos = best[1].origin.coordinate_end
      if best[1].f > f_limit:
        return [None, best[1].f]
      if len(successors) != 0:
        alternative = nsmallest(1, successors)[0][0]
      else:
        alternative = math.inf
      [result,best[1].f] = RBFS(state, best[1], goalnode, min(f_limit, alternative))
      if result != None:
        return [result, None]


if __name__ == '__main__':
    u = _Utilities().load_all(
        sizes=[(i,j) for i in range(4,9) for j in range(4,9)],
        directory='AI_intro_project/randomized_states',
        extension='state'
    )
    t = []
    #ko giải được 41?
    for i in range(50):
      z = []
      m = 0
      s = u[i]
      #s =State()
      #s.initialize_4x4_default()

      startnode = Node(s.walked_moves[-1], s.current_tax)
      #goalnode = Node(Move(s.board_size[0], s.board_size[1]-1, 'R') , 0)
      goalnode = Node(Move(s.board_size[0]-1, s.board_size[1], 'D'), 0)

      solution = RBFS(s, startnode, goalnode, math.inf)
      if solution[0] != None:

        for k in solution[0].pathway():
            s.walked_moves.append(k)
        s.current_tax = solution[0].g
      else:
        for k in min(z)[1].pathway():
            s.walked_moves.append(k)
        s.current_tax = min(z)[0]


      print('Số lần đến đích: ', len(z))
      print('Số vòng recursive thực hiện', m)
      t.append((m, len(z), len(s.walked_moves), s.current_tax))

    #   s.visualize()

    print(t)