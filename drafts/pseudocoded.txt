(Coordinate, Move thêm __hash__ và __repr__)

class Node(status: Move, g: float, path: list(), goal: tuple())
   def init(status, g = 0, path =[], goal =(0,0))
      self.status = status
      self.g = g 
      self.path = path
      self.goal = goal
      self.h = 0  
      self.f = 0
      self.depth = 0 
      self.parent = parent
      if parent: 
         self.depth = parent + 1
   def eq,str,...
   def child_node_list: 
      return [Node(child) for child in availble_list_move]
   def h: 
      '''m chẵn phải (m/2 - g), xuống n-1, phải m/2, lên n-1

         trái (m/2 -1), xuống 1, trái (m/2 + 1)

         Xuống n-1, phải m

	 m lẻ phải ((m-1)/2 - g), xuống n-1, phải (m+1)/2, lên n-1

	 trái ((m-1)/2 -1), xuống 1, trái ((m-1)/2 + 1)

         Xuống n-1, phải m'''

      m = goal[0] - self.status.x
      n = goal[1] - self.status.y
      if m % 2 == 0
      	self.h = ((((((2*(m/2))*(2**(n-1))+2*(m/2))/(2**(n-1)))-((m/2)-1)*2)*2 - ((m/2)+1)*2)*(2**(n-1))) + 2*m
      else
	self.h = ((((((2*(m-1)/2))*(2**(n-1))+2*(m+1)/2))/(2**(n-1)))-((m-1)/2)-1)*2)*2 - ((m-1)/2)+1)*2)*(2**(n-1))) + 2*m 
      return self.h 
   def path: 
      node = self
      while node:  
            self.path.append(node.status)  
            node = node.parent 
      return [reversed(path)] 
    
  
def RBFS(startnode: Node, goalnode: Node, f_limit: float) return [Node, f_limit]
   if startnode.status == goalnode.status and startnode.h == 0: return[startnode, None]
   successors = PriorityQueue()
   successors.put((startnode.h, startnode))
   for child in startnode.child_node_list
      child.f = child.g + child.h
      successors.put((child.f,child))
   if successors.qsize == 0: return [None, inf]
   while True:
      nextNode = successors.get()
      if nextNode.f > f_limit: return [None, nextNode.f]
      alternative = successors[0]
      [result ,nextNode.f] = RBFS(state, nextNode, min(f_limit, alternative))
      if result != None: return [result, None]


if __name__ == '__main__':
    s = State()
    s.initialize_4*4_default 
    startnode = Node(s.walked_moves[0], s.current_tax, s.walked_moves,s.boardsize)
    goalnode = Node(Move(s.boardsize[0]-1, s.boardsize[1], 'L') , 0)   or Node(Move(s.boardsize[0], s.boardsize[1]-1, 'D'), 0) 
    solution = RBFS(startnode, goalnode, math.inf)
    if solution[0] != None:
       print(solution[0].path, solution[0].g)
       
   #Add new event to play.py
    event == 'mxn (random)':
        plt.clf()

        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()

        fig.set_size_inches(808 * 2 / float(DPI), 808 / float(DPI))

        s = State()
        s.initialize_mxn_random()
        startnode = Node(s.walked_moves[0], s.current_tax, s.walked_moves,s.boardsize)
        goalnode = Node(Move(s.boardsize[0]-1, s.boardsize[1], 'L') , 0)   or Node(Move(s.boardsize[0], s.boardsize[1]-1, 'D'), 0) 
        solution = RBFS(startnode, goalnode, math.inf)
        if solution[0] != None:
            [s.walked_moves, s.current_tax] = [solution[0].path, solution[0].g]
        else: 
            raise RuntimeError
        s._plt_prepare()

        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
 
       
    
