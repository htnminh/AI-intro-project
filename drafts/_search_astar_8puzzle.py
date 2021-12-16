from queue import PriorityQueue
from time import time

# 8-puzzle
class Puzzle:
    goal_state=\
        [1, 2, 3,
         4, 5, 6,
         7, 8, 0]
    heuristic=None
    evaluation_function=None
    needs_heuristic=False
    num_of_instances=0

    def __init__(self, state, parent, action, path_cost, needs_heuristic=False):
        self.parent=parent
        self.state=state
        self.action=action
        if parent:
            self.path_cost = parent.path_cost + path_cost
        else:
            self.path_cost = path_cost
        if needs_heuristic:
            self.needs_heuristic=True
            self.generate_heuristic()
            self.evaluation_function=self.heuristic+self.path_cost
        Puzzle.num_of_instances+=1

    def __str__(self):
        return str(self.state[0:3])+'\n'+str(self.state[3:6])+'\n'+str(self.state[6:9])

    def generate_heuristic(self):
        self.heuristic=0
        for num in range(1,9):
            distance=abs(self.state.index(num) - self.goal_state.index(num))
            i=int(distance/3)
            j=int(distance%3)
            self.heuristic=self.heuristic+i+j

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    @staticmethod
    def find_legal_actions(i,j):
        legal_action = ['U', 'D', 'L', 'R']
        if i == 0:  # up is disable
            legal_action.remove('U')
        elif i == 2:  # down is disable
            legal_action.remove('D')
        if j == 0:
            legal_action.remove('L')
        elif j == 2:
            legal_action.remove('R')
        return legal_action

    def generate_child(self):
        children=[]
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions=self.find_legal_actions(i,j)

        for action in legal_actions:
            new_state = self.state.copy()
            if action == 'U':
                new_state[x], new_state[x-3] = new_state[x-3], new_state[x]
            elif action == 'D':
                new_state[x], new_state[x+3] = new_state[x+3], new_state[x]
            elif action == 'L':
                new_state[x], new_state[x-1] = new_state[x-1], new_state[x]
            elif action == 'R':
                new_state[x], new_state[x+1] = new_state[x+1], new_state[x]
            children.append(Puzzle(new_state, self, action, 1, self.needs_heuristic))
        return children

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution

# A*
def Astar_search(initial_state):
    print("hello!")
    count=0
    explored=[]
    start_node=Puzzle(initial_state, None, None, 0, True)
    q = PriorityQueue()
    q.put((start_node.evaluation_function, count, start_node))

    while not q.empty():
        node=q.get()
        node=node[2]
        explored.append(node.state)
        if node.goal_test():
            return node.find_solution()

        children=node.generate_child()
        for child in children:
            if child.state not in explored:
                count += 1
                q.put((child.evaluation_function, count, child))
    return

if __name__ == '__main__':
    state=\
        [0, 2, 3,
         4, 1, 6,
         7, 5, 8]

    # output: moving 0 around
    Puzzle.num_of_instances = 0
    t0 = time()
    astar = Astar_search(state)
    t1 = time() - t0
    print('A*:',astar)
    print('space:', Puzzle.num_of_instances)
    print('time:', t1)