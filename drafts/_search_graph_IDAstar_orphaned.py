import math
import time
from random import randint
import os
import pygame

# init pygame for visual
pygame.init()

# init visual map
MARGIN = 2
[GRID_SIZE, GRID_X, GRID_Y] = [10, 50, 50]
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 204, 204)

def drawRect(color, x, y, screen):
    pygame.draw.rect(screen, color,
                     [(MARGIN + GRID_SIZE) * x + MARGIN,
                      (MARGIN + GRID_SIZE) * y + MARGIN,
                      GRID_SIZE, GRID_SIZE])

def drawMap(grid, start, goal, screen, percent_chance_for_obstacle=10):
    for x in range(GRID_X):
        for y in range(GRID_Y):
            if grid[x][y] != start and grid[x][y] != goal:
                if randint(1, 100) <= percent_chance_for_obstacle:
                    grid[x][y].setObstacle()
            if getNorthGrid(grid, x, y, GRID_Y):
                grid[x][y].children.append(getNorthGrid(grid, x, y, GRID_Y))
            if getSouthGrid(grid, x, y, GRID_Y):
                grid[x][y].children.append(getSouthGrid(grid, x, y, GRID_Y))
            if getWestGrid(grid, x, y, GRID_X):
                grid[x][y].children.append(getWestGrid(grid, x, y, GRID_X))
            if getEastGrid(grid, x, y, GRID_X):
                grid[x][y].children.append(getEastGrid(grid, x, y, GRID_X))
            if getNorthWestGrid(grid, x, y, GRID_X, GRID_Y):
                grid[x][y].children.append(
                    getNorthWestGrid(grid, x, y, GRID_X, GRID_Y))
            if getNorthEastGrid(grid, x, y, GRID_X, GRID_Y):
                grid[x][y].children.append(
                    getNorthEastGrid(grid, x, y, GRID_X, GRID_Y))
            if getSouthWestGrid(grid, x, y, GRID_X, GRID_Y):
                grid[x][y].children.append(
                    getSouthWestGrid(grid, x, y, GRID_X, GRID_Y))
            if getSouthEastGrid(grid, x, y, GRID_X, GRID_Y):
                grid[x][y].children.append(
                    getSouthEastGrid(grid, x, y, GRID_X, GRID_Y))
    for x in range(GRID_X):
        for y in range(GRID_Y):
            if x == start.x and y == start.y:
                drawRect(GREEN, x, y, screen)
            elif x == goal.x and y == goal.y:
                drawRect(RED, x, y, screen)
            elif grid[x][y].isObstacle:
                drawRect(BLACK, x, y, screen)
            else:
                drawRect(WHITE, x, y, screen)

# Grids
def getNorthGrid(grid, x, y, GRID_Y):
    if y < GRID_Y - 1 and not grid[x][y+1].isObstacle:
        return grid[x][y+1]

def getSouthGrid(grid, x, y, GRID_Y):
    if y > 0 and not grid[x][y-1].isObstacle:
        return grid[x][y-1]

def getWestGrid(grid, x, y, GRID_X):
    if x > 0 and not grid[x-1][y].isObstacle:
        return grid[x-1][y]

def getEastGrid(grid, x, y, GRID_X):
    if x < GRID_X - 1 and not grid[x+1][y].isObstacle:
        return grid[x+1][y]

def getNorthWestGrid(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y < GRID_Y - 1 and not grid[x-1][y+1].isObstacle:
        return grid[x-1][y+1]

def getNorthEastGrid(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y < GRID_Y - 1 and not grid[x+1][y+1].isObstacle:
        return grid[x+1][y+1]

def getSouthWestGrid(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y > 0 and not grid[x-1][y-1].isObstacle:
        return grid[x-1][y-1]

def getSouthEastGrid(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y > 0 and not grid[x+1][y-1].isObstacle:
        return grid[x+1][y-1]

# Node || Todo: -
class Node:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.parent = None
        self.H = 0
        self.G = 0
        self.children = []
        self.isObstacle = False
        self.start = False
        self.goal = False

    def cost(self):
        if self.parent:
            return int(math.sqrt((self.x - self.parent.x) ** 2) + math.sqrt(
                (self.y - self.parent.y) ** 2))
        else:
            return 0

    def isWall(self):
        return self.isObstacle

    def setWall(self):
        self.isObstacle = True

    def isStart(self):
        return self.start

    def setStart(self):
        self.start = True

    def isGoal(self):
        return self.goal

    def setGoal(self):
        self.goal = True

def ED(current, goal):
    if not current == goal:
        return int(math.sqrt((goal.x - current.x) ** 2) + math.sqrt((goal.y - current.y) ** 2))
    else:
        return 0

# Anytime Repairing A*
def araStar(start, goal):

    openList = set()
    closedList = set()
    incumbent = []
    # s
    current = start

    # sets the start nodes heuristic
    current.H = ED(current, goal)

    # adds start to open list
    openList.add(current)

    # G
    pathCost = 10000000000

    # w0
    temp = max(openList, key=lambda o: (pathCost - o.G) / o.H)
    weight = 300000
    weightDelta = weight / 10

    # while there are nodes in the open list
    while openList:
        tempList = openList
        NewSolution = improvedSolution(goal, tempList, weight, pathCost)

        if NewSolution:
            pathCost = NewSolution[-1].G
            incumbent = NewSolution
            drawPath(incumbent, randomColor())
            time.sleep(.5)
        else:
            return incumbent
        weight = weight - weightDelta

    return incumbent


def improvedSolution(goal, openList, weight, pathCost):
    closedList = set()
    # while there are nodes in the open list
    while openList:

        current = min(openList, key=lambda o: o.G + weight * o.H)

        openList.remove(current)
        closedList.add(current)

        # exits function if estimated travel is more than best path cost
        if pathCost < current.G + weight * current.H:
            # pathCost is proven to be w-admissable
            return None

        # for each child
        for node in current.children:
            # Duplicate detection and updating g(n`)
            if node.isObstacle:
                continue
            if node in closedList and node.G < current.G + node.cost():
                continue
            if node in openList and node.G < current.G + node.cost():
                continue
            if current.parent:
                current.G = current.parent.G + current.cost()

            # Prune nodes over the bound
            if node.G + node.H > pathCost:
                continue
            if node in openList:
                new_g = current.G + node.cost()
                if node.G > new_g:
                    node.G = new_g
                    node.parent = current
            else:
                node.parent = current
                node.G = current.G + node.cost()
                if not node == goal:
                    node.H = ED(node, goal)
                else:
                    node.H = 1
                    path = []
                    while node.parent:
                        node = node.parent
                        path.append(node)
                    path.append(node)
                    return path[::-1]
                openList.add(node)
    return None


def drawRect(color, x, y):
    pygame.draw.rect(screen,
                     color,
                     [(MARGIN + GRID_SIZE) * x + MARGIN,
                      (MARGIN + GRID_SIZE) * y + MARGIN,
                      GRID_SIZE,
                      GRID_SIZE])


def north(grid, x, y, GRID_Y):
    if y > 0 and not grid[x][y - 1].isObstacle:
        return grid[x][y - 1]


def south(grid, x, y, GRID_Y):
    if y < GRID_Y - 1 and not grid[x][y + 1].isObstacle:
        return grid[x][y + 1]


def west(grid, x, y, GRID_X):
    if x > 0 and not grid[x - 1][y].isObstacle:
        return grid[x - 1][y]


def east(grid, x, y, GRID_X):
    if x < GRID_X - 1 and not grid[x + 1][y].isObstacle:
        return grid[x + 1][y]


def northEast(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y > 0 and not grid[x + 1][y - 1].isObstacle:
        return grid[x + 1][y - 1]


def southEast(grid, x, y, GRID_X, GRID_Y):
    if x < GRID_X - 1 and y < GRID_Y - 1 and not grid[x + 1][y + 1].isObstacle:
        return grid[x + 1][y + 1]


def northWest(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y > 0 and not grid[x - 1][y - 1].isObstacle:
        return grid[x - 1][y - 1]


def southWest(grid, x, y, GRID_X, GRID_Y):
    if x > 0 and y < GRID_Y - 1 and not grid[x - 1][y + 1].isObstacle:
        return grid[x - 1][y + 1]


def drawPath(path, color):
    for p in path:
        if not p == S and not p == G:
            drawRect(color, p.x, p.y)
            pygame.display.update()

def randomColor():
    return randint(0, 255), randint(0, 255), randint(0, 255)

# Modifies variables here
GRID_SIZE = 10
GRID_X = 50
GRID_Y = 50
MARGIN = 2
os.environ['SDL_VIDEO_CENTERED'] = '1'
screen = pygame.display.set_mode(
    (GRID_X * GRID_SIZE + GRID_X * MARGIN + MARGIN, GRID_Y * GRID_SIZE + GRID_Y * MARGIN + MARGIN), pygame.RESIZABLE)
pygame.display.set_caption('A* Algorithm')
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 204, 204)
percentChanceForWall = 30
actualPercentOfWalls = 0

grid = [[Node(i, j, '') for i in range(GRID_X)] for j in range(GRID_Y)]

S = grid[GRID_X - 1][0]
G = grid[0][GRID_Y - 1]

for x in range(GRID_X):
    for y in range(GRID_Y):
        if grid[x][y] != S and grid[x][y] != G:
            if randint(1, 100) <= percentChanceForWall:
                grid[x][y].setWall()
                actualPercentOfWalls = actualPercentOfWalls + 1
        if getNorthGrid(grid, x, y, GRID_Y):
            grid[x][y].children.append(getNorthGrid(grid, x, y, GRID_Y))
        if getSouthGrid(grid, x, y, GRID_Y):
            grid[x][y].children.append(getSouthGrid(grid, x, y, GRID_Y))
        if getWestGrid(grid, x, y, GRID_X):
            grid[x][y].children.append(getWestGrid(grid, x, y, GRID_X))
        if getEastGrid(grid, x, y, GRID_X):
            grid[x][y].children.append(getEastGrid(grid, x, y, GRID_X))
        if getNorthEastGrid(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(getNorthEastGrid(grid, x, y, GRID_X, GRID_Y))
        if getNorthWestGrid(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(getNorthWestGrid(grid, x, y, GRID_X, GRID_Y))
        if getSouthEastGrid(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(getSouthEastGrid(grid, x, y, GRID_X, GRID_Y))
        if getSouthWestGrid(grid, x, y, GRID_X, GRID_Y):
            grid[x][y].children.append(getSouthWestGrid(grid, x, y, GRID_X, GRID_Y))

for x in range(GRID_X):
    for y in range(GRID_Y):
        if grid[y][x].isObstacle:
            drawRect(BLACK, x, y)
        else:
            drawRect(WHITE, x, y)
        if x == 0 and y == GRID_Y - 1:
            drawRect(GREEN, x, y)
        if x == GRID_X - 1 and y == 0:
            drawRect(RED, x, y)

pygame.display.flip()
startTime = time.time()
path = araStar(S, G)
print("It took %s seconds to run" % (time.time() - startTime))
if path:
    drawPath(path, BLUE)
else:
    print('No path from start to goal.')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()