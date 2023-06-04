# -------------------------------* IMPORT *-------------------------------
from collections import deque
import sys

# -------------------------------* CELL CLASS *-------------------------------
class Cell(object):
    index: int
    cell_type: int
    resources: int
    neighbors: list[int]
    my_ants: int
    opp_ants: int

    def __init__(self, index: int, cell_type: int, resources: int, neighbors: list[int], my_ants: int, opp_ants: int):
        self.index = index
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors
        self.my_ants = my_ants
        self.opp_ants = opp_ants

# -------------------------------* GAME CLASS *-------------------------------
class Game(object):
    cells: list[Cell] = []

    def __init__(self, cells):
        self.cells = cells

    def sum_cry(self):
        return sum(cell.resources for cell in self.cells if cell.cell_type == 2)

    def sum_eggs(self):
        return sum(cell.resources for cell in self.cells if cell.cell_type == 1)

    def sum_opp_ants(self):
        return sum(cell.opp_ants for cell in self.cells)

    def sum_my_ants(self):
        return sum(cell.my_ants for cell in self.cells)

    def count_cry(self):
        return sum(1 for cell in self.cells if cell.cell_type == 2)

    def count_eggs(self):
        return sum(1 for cell in self.cells if cell.cell_type == 1)
    
    def bfs(self, start_index, target_type):
        visited = set()
        queue = deque([(start_index, [start_index])])
        paths = {}
        while queue:
            current_index, path = queue.popleft()
            current_cell = self.cells[current_index]
            visited.add(current_index)

            if current_cell.cell_type == target_type:
                if current_index in paths and len(path) >= len(paths[current_index]):
                    continue
                paths[current_index] = path
            for neighbor_index in current_cell.neighbors:
                if neighbor_index not in visited:
                    queue.append((neighbor_index, path + [neighbor_index]))
        return list(paths.values())
    
    def get_safe_part(self,base ,dist_bet_bases, target_type):
        paths = game.bfs(base, target_type)
        safe_paths = []
        for path in paths:
            if  len(path) < dist_bet_bases // 2:
                safe_paths.append(path)
        return safe_paths
    
    def get_middle_part(self, base, dist_bet_bases, target_type):
        paths = game.bfs(base, target_type)
        safe_paths = []
        for path in paths:
            if  len(path) <= round(dist_bet_bases / 2):
                safe_paths.append(path)
        return safe_paths 


# -------------------------------* INFOS *-------------------------------

cells: list[Cell] = []
game = Game(cells=cells)
number_of_cells = int(input())
for i in range(number_of_cells):
    inputs = [int(j) for j in input().split()]
    cell_type = inputs[0]
    initial_resources = inputs[1]
    neigh_0 = inputs[2]
    neigh_1 = inputs[3]
    neigh_2 = inputs[4]
    neigh_3 = inputs[5]
    neigh_4 = inputs[6]
    neigh_5 = inputs[7]
    cell: Cell = Cell(
        index = i,
        cell_type = cell_type,
        resources = initial_resources,
        neighbors = list(filter(lambda id: id > -1,[neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5])),
        my_ants = 0,
        opp_ants = 0
    )
    game.cells.append(cell)
number_of_bases = int(input())
my_bases: list[int] = []
for i in input().split():
    my_base_index = int(i)
    my_bases.append(my_base_index)
opp_bases: list[int] = []
for i in input().split():
    opp_base_index = int(i)
    opp_bases.append(opp_base_index)


# -------------------------------* GLOBAL VARIABLES *-------------------------------
cry_init = sum(cell.resources for cell in game.cells if cell.cell_type == 2)
eggs_init = sum(cell.resources for cell in game.cells if cell.cell_type == 1)



# -------------------------------* GAME LOOP *-------------------------------


if len(my_bases) == 2:
    game.cells[opp_bases[0]].cell_type = -1
    dist_1 = len(game.bfs(my_bases[1], -1)[0])
    print(game.bfs(my_bases[1], -1)[0], file = sys.stderr)

    game.cells[opp_bases[1]].cell_type = -2
    dist_2 = len(game.bfs(my_bases[0], -2)[0])
    print(game.bfs(my_bases[0], -2)[0], file = sys.stderr)
    
else :
    game.cells[opp_bases[0]].cell_type = -1
    dist_1 = len(game.bfs(my_bases[0], -1)[0])


while True:
    # ******** Init Cells ********
    myScore, oppScore = map(int, input().split())
    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]
        resources = inputs[0]
        my_ants = inputs[1]
        opp_ants = inputs[2]
        game.cells[i].resources = resources
        game.cells[i].my_ants = my_ants
        game.cells[i].opp_ants = opp_ants

    # ******** Implementation ********
    actions = []
    for index, base in enumerate(my_bases):
        for cell in cells:
            if cell.resources == 0:
                cell.cell_type = 0
        if round(eggs_init * 0.10) > (game.sum_my_ants() - 10) :
            if index == 0:
                safe_path = game.get_safe_part(base, dist_1, 1)
            else:
                safe_path = game.get_safe_part(base, dist_2, 1)
            for path in safe_path:
                if game.cells[path[-1]].resources :
                    actions.append(f"LINE {base} {path[-1]} 1")
                else:
                    game.cells[path[-1]].cell_type = 0

        if len(actions) == 0:
            if index == 0:
                mid_path = game.get_middle_part(base, dist_1, 1)
                safe_path = game.get_safe_part(base, dist_1, 1)
            else:
                mid_path = game.get_middle_part(base, dist_2, 1)
                safe_path = game.get_safe_part(base, dist_2, 1)

            mid_part = []
            for middle in mid_path:
                if middle not in safe_path:
                    mid_part.append(middle)
                    
            if index == 0:
                safe_path = game.get_safe_part(base, dist_1, 2)
            else:
                safe_path = game.get_safe_part(base, dist_2, 2)

            for path in safe_path:
                if game.cells[path[-1]].resources :
                    actions.append(f"LINE {base} {path[-1]} 1")
                else:
                    game.cells[path[-1]].cell_type = 0
            if len(actions) == 0:
                if index == 0:
                    mid_path = game.get_middle_part(base, dist_1, 2)
                    safe_path = game.get_safe_part(base, dist_1, 2)
                else:
                    mid_path = game.get_middle_part(base, dist_2, 2)
                    safe_path = game.get_safe_part(base, dist_2, 2)
                mid_part = []
                for middle in mid_path:
                    if middle not in safe_path:
                        mid_part.append(middle)
                for path in mid_part:
                    if game.cells[path[-1]].resources :
                        actions.append(f"LINE {base} {path[-1]} 1")
                    else:
                        game.cells[path[-1]].cell_type = 0


            for path in mid_part:
                if game.cells[path[-1]].resources :
                    actions.append(f"LINE {base} {path[-1]} 1")
                else:
                    game.cells[path[-1]].cell_type = 0
            print(len(actions), file = sys.stderr)

        if len(actions) == 0:
            paths = game.bfs(base, 2)
            for path in range(len(paths)):
                if game.cells[paths[path][-1]].resources :
                    actions.append(f"LINE {base} {paths[path][-1]} 1")
                else:
                    game.cells[paths[path][-1]].cell_type = 0
    
    if len(actions) == 0:
        print("WAIT")
    else:
        print(";".join(actions))
