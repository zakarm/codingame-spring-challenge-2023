from collections import deque

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

cells: list[Cell] = []

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
    cells.append(cell)

number_of_bases = int(input())
my_bases: list[int] = []

for i in input().split():
    my_base_index = int(i)
    my_bases.append(my_base_index)

opp_bases: list[int] = []
for i in input().split():
    opp_base_index = int(i)
    opp_bases.append(opp_base_index)

def bfs(cells, start_index, target_type):
    visited = set()
    queue = deque([(start_index, [start_index])])
    paths = {}
    while queue:
        current_index, path = queue.popleft()
        current_cell = cells[current_index]
        visited.add(current_index)
        if current_cell.cell_type == target_type:
            if current_index in paths and len(path) >= len(paths[current_index]):
                continue
            paths[current_index] = path
        for neighbor_index in current_cell.neighbors:
            if neighbor_index not in visited:
                queue.append((neighbor_index, path + [neighbor_index]))
    return list(paths.values())

c = sum(cell.resources for cell in cells if cell.cell_type == 2)
d = sum(cell.resources for cell in cells if cell.cell_type == 1)

tester = 0
def len_c():
    return sum(cell.resources for cell in cells if cell.cell_type == 2)
def len_d():
    count = 0
    for cell in cells:
        if cell.cell_type == 1:
            count += 1
    return count

while True:
    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]
        resources = inputs[0]
        my_ants = inputs[1]
        opp_ants = inputs[2]
        cells[i].resources = resources
        cells[i].my_ants = my_ants
        cells[i].opp_ants = opp_ants
    actions = []
    if len_c() <= 4:
        percent = 0.9
    else:
        percent = 0.8
    if round(c * percent) < len_c() :
        if cells[0].resources and cells[0].cell_type == 1:
            actions.append(f"LINE {my_bases[0]} {0} 1")
        paths = bfs(cells, my_bases[0], 1)
        len_pi = len_d() / 2
        if len_pi % 2 != 0 and len_pi != 1:
            len_pi += 1
        for i in range(round(len_pi)):
            if cells[paths[i][-1]].resources:
                actions.append(f"LINE {cells[my_bases[0]].index} {cells[paths[i][-1]].index} {cells[paths[i][-1]].resources // 2}")
                tester += 1
    if len(actions) == 0:
        pathss = bfs(cells, my_bases[0], 2)
        if pathss:
            for path in pathss:
                if cells[path[-1]].resources and cells[path[-1]].cell_type == 2:
                    actions.append(f"LINE {cells[my_bases[0]].index} {cells[path[-1]].index} 1")
    if len(actions) == 0:
        print()
    else:
        print(";".join(actions))
