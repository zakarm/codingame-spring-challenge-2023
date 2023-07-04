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


c = sum(cell.resources for cell in game.cells if cell.cell_type == 2)
d = sum(cell.resources for cell in game.cells if cell.cell_type == 1)

# -------------------------------* GAME LOOP *-------------------------------
while True:
    myScore, oppScore = input().split()
    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]
        resources = inputs[0]
        my_ants = inputs[1]
        opp_ants = inputs[2]
        game.cells[i].resources = resources
        game.cells[i].my_ants = my_ants
        game.cells[i].opp_ants = opp_ants
    actions = []

    for base in my_bases:
        if game.count_cry() <= 4:
            percent = 0.9
        else:
            percent = 0.8
        boolean = False
        for cell in game.cells:
            if cell.resources == 0:
                cell.cell_type = 0
        for nei in game.cells[base].neighbors:
            for k in game.cells[nei].neighbors:
                if game.cells[k].cell_type == 1 and game.cells[k].resources:
                    actions.append(f"LINE {base} {game.cells[k].index} 1")
                    boolean = True
                elif game.cells[nei].resources == 0:
                    game.cells[nei].cell_type = 0
        if round(c * percent) < game.sum_cry() and boolean == False and game.count_cry() > 1:
            if len(my_bases) == 2:
                paths = game.bfs(base, 1)
                len_pi = game.count_eggs() / 4
                if len_pi % 2 != 0 and len_pi != 1:
                    len_pi += 1
                for i in range(round(len_pi)):
                    if i in range(len(paths)):
                        if game.cells[paths[i][-1]].resources :
                            actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                        else :
                            game.cells[paths[i][-1]].cell_type = 0
            else:
                paths = game.bfs(base, 1)
                len_pi = game.count_eggs() / 2
                for i in range(round(len_pi) + 2):
                    if i in range(len(paths)):
                        if game.cells[paths[i][-1]].resources:
                            actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} {game.cells[paths[i][-1]].resources}")
                        else :
                            game.cells[paths[i][-1]].cell_type = 0
        if (len(actions) == 0 and boolean == False) or game.count_eggs() == 0:
            paths = game.bfs(base, 2)
            len_pic = game.count_cry() / 2
            if len_pic % 2 != 0 and len_pic != 1:
                len_pic += 1
            if paths:
                for i in range(round(len_pic)):
                    if i in range(len(paths)):
                        if game.cells[paths[i][-1]].resources and game.cells[paths[i][-1]].cell_type == 2:
                            actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                        elif game.cells[paths[i][-1]].resources == 0 :
                            game.cells[paths[i][-1]].cell_type = 0
        

    if len(actions) == 0:
        print("WAIT")
    else:
        print(";".join(actions))