# -*- coding: utf-8 -*-
from typing import Protocol, Dict, List, Iterator, Tuple, TypeVar, Optional
import heapq
from random import randint

T = TypeVar('T')

Location = TypeVar('Location')
class Graph(Protocol):
    def neighbors(self, id: Location) -> List[Location]: pass

GridLocation = Tuple[int, int]

class SquareGrid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.walls: List[GridLocation] = []
    
    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height
    
    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls
    
    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results

class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass

class GridWithWeights(SquareGrid):
    def __init__(self, width: int, height: int):
        super().__init__(width, height)
        self.weights: Dict[GridLocation, float] = {}
    
    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)
    
class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []
    
    def empty(self) -> bool:
        return not self.elements
    
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]
    
def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from: Dict[Location, Location],
                     start: Location, goal: Location) -> List[Location]:
    current: Location = goal
    path: List[Location] = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while not frontier.empty():
        current: Location = frontier.get()
        
        if current == goal:
            break
        
        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current
                
    return came_from, cost_so_far

def draw_tile(graph, id, style):
    r = " . "
    if 'number' in style and id in style['number']: r = " %-2d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = " > "
        if x2 == x1 - 1: r = " < "
        if y2 == y1 + 1: r = " v "
        if y2 == y1 - 1: r = " ^ "
    if 'path' in style and id in style['path']:   r = " @ "
    if 'start' in style and id == style['start']: r = " A "
    if 'goal' in style and id == style['goal']:   r = " Z "
    if id in graph.walls: r = "###"
    return r

def draw_grid(graph, **style):
    print("___" * graph.width)
    for y in range(graph.height):
        for x in range(graph.width):
            print("%s" % draw_tile(graph, (x, y), style), end="")
        print()
    print("~~~" * graph.width)

def posizioneCasualeAmbulanza(posizioneOstacoli, posizionePaziente):
    cordinataAmbulanza = (randint(0, 9), randint(0, 9))
    
    while(cordinataAmbulanza in posizioneOstacoli 
          or cordinataAmbulanza == posizionePaziente):
        cordinataAmbulanza = (randint(0, 9), randint(0, 9))
    
    return cordinataAmbulanza

def costruisciPercorsoVie(percorsoCompleto, indrizzoVia):
    percorsoVie = list()
    
    for posizione in percorsoCompleto:
        percorsoVie.append((indrizzoVia.get(posizione[1]), posizione[0]))
    print(percorsoVie)
        

# ----------------------------------------------
diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 1), (1, 2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8),
                  (2,8),
                  (3,6), (3,0), (3,1),(3,2),(3,3), (3,8),
                  (4,8), 
                  (5,0), (5,1),(5,2),(5,3),(5,4),(5,5),(5,6),
                  (7,3), (7,4),(7,5),(7,6),(7,7),(7,8),
                  (9,0), (9,1), (9,2), (9,6), (9,7), (9,8), (9,9)]

diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

goal = (7, 1)
start = posizioneCasualeAmbulanza(diagram4.walls, goal)
print(start)

came_from, cost_so_far = a_star_search(diagram4, start, goal)

viaIndirizzo = { "Via Capruzzi": 0,
    "Via Policlinico": 1,
    "Viale Aviatori": 2,
    "Via Marcuzzi": 3,
    "Via Napoli": 4,
    "Corso Roma": 5,
    "Via Lattea": 6,
    "Via degli Dei": 7,
    "Via delle querce": 8,
    "Viale del Todis": 9,
    "Corso Umberto Primo": 10 }

indrizzoVia = {0:"Via Capruzzi",
    1:"Via Policlinico",
    2:"Viale Aviatori",
    3:"Via Marcuzzi",
    4:"Via Napoli",
    5:"Corso Roma",
    6:"Via Lattea",
    7:"Via degli Dei",
    8:"Via delle querce",
    9:"Viale del Todis",
    10:"Corso Umberto Primo"}

draw_grid(diagram4, point_to=came_from, start=start, goal=goal)
print()
draw_grid(diagram4, path=reconstruct_path(came_from, start=start, goal=goal))

#draw_grid(diagram4, number=cost_so_far, start=start, goal=goal)

path=reconstruct_path(came_from, start=start, goal=goal)

costruisciPercorsoVie(path, indrizzoVia)











