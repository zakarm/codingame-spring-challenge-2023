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


cry_init = sum(cell.resources for cell in game.cells if cell.cell_type == 2)
eggs_init = sum(cell.resources for cell in game.cells if cell.cell_type == 1)

# cry_coll =
# eggs_coll =

# -------------------------------* GAME LOOP *-------------------------------
while True:
    myScore, oppScore = map(int, input().split())
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
        percent = 0.8

        boolean = False
        for cell in game.cells:
            if cell.resources == 0:
                cell.cell_type = 0
        for nei in game.cells[base].neighbors:
            for k in game.cells[nei].neighbors:
                if game.cells[k].cell_type == 1 and game.cells[k].resources :#and round(eggs_init * 0.20) > (game.sum_my_ants() - 10):
                    actions.append(f"LINE {base} {game.cells[k].index} 3")
                    boolean = True
                elif game.cells[nei].resources == 0:
                    game.cells[nei].cell_type = 0
        if round(eggs_init * 0.20) > (game.sum_my_ants() - 10) and boolean == False:
            # print(f"{round(eggs_init * 0.15)} {game.sum_my_ants() - 10}", file = sys.stderr)
            if len(my_bases) == 2:
                paths = game.bfs(base, 1)
                len_pi = game.count_eggs() / 4
                for i in range(round(len_pi)):
                    if i in range(len(paths)):
                        if game.cells[paths[i][-1]].resources :
                            actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                        else :
                            game.cells[paths[i][-1]].cell_type = 0
            else :
                paths = game.bfs(base, 1)
                len_pi = game.count_eggs() / 2
                print(f"{len_pi}", file=sys.stderr)
                for i in range(round(len_pi)):
                    if i in range(len(paths)):
                        if game.cells[paths[i][-1]].resources:
                            actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                        else :
                            game.cells[paths[i][-1]].cell_type = 0
        if len(actions) == 0:
            if len(my_bases) == 2:
                paths = game.bfs(base, 2)
                count_cry_2 = game.count_cry() / 4
                if paths:
                    for i in range(round(count_cry_2)):
                        if i in range(len(paths)):
                            if game.cells[paths[i][-1]].resources and game.cells[paths[i][-1]].cell_type == 2:
                                actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                            elif game.cells[paths[i][-1]].resources == 0 :
                                game.cells[paths[i][-1]].cell_type = 0
                if count_cry_2 > 1:
                    paths = game.bfs(base, 1)
                    len_pi = game.count_eggs() / 1.5
                    for i in range(round(len_pi)):
                        if i in range(len(paths)):
                            if game.cells[paths[i][-1]].resources:
                                actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                            else :
                                game.cells[paths[i][-1]].cell_type = 0
            else :
                paths = game.bfs(base, 2)
                if game.count_cry() == 3:
                    count_cry_2 = game.count_cry() / 3
                elif game.count_cry() == 2:
                    count_cry_2 = game.count_cry() / 2
                elif game.count_cry() == 1:
                    count_cry_2 = game.count_cry()
                else :
                    count_cry_2 = game.count_cry() / 4
                if paths:
                    for i in range(round(count_cry_2)):
                        if i in range(len(paths)):
                            if game.cells[paths[i][-1]].resources and game.cells[paths[i][-1]].cell_type == 2:
                                actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                            elif game.cells[paths[i][-1]].resources == 0 :
                                game.cells[paths[i][-1]].cell_type = 0
                if count_cry_2 > 1:
                    paths = game.bfs(base, 1)
                    len_pi = game.count_eggs() / 3
                    for i in range(round(len_pi)):
                        if i in range(len(paths)):
                            if game.cells[paths[i][-1]].resources:
                                actions.append(f"LINE {base} {game.cells[paths[i][-1]].index} 1")
                            else :
                                game.cells[paths[i][-1]].cell_type = 0

    if len(actions) == 0:
        print("WAIT")
    else:
        print(";".join(actions))
