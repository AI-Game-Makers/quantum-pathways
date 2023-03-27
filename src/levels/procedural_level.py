import random
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.breadth_first import BreadthFirstFinder


class ProceduralLevel:
    def __init__(self,id, width, height):
        random.seed(id)  # Seed the random number generator for reproducibility.
        self.id = id
        self.width = width
        self.height = height
        self.grid = self.generate()

    def generate_maze(self, width, height):
        maze = np.zeros((height, width), dtype=bool)

        if width % 2 == 0:
            width -= 1
        if height % 2 == 0:
            height -= 1

        maze.fill(False)

        frontier = []

        start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
        maze[start_y, start_x] = True
        frontier.extend([(start_x + 2, start_y), (start_x - 2, start_y), (start_x, start_y + 2), (start_x, start_y - 2)])

        while frontier:
            x, y = random.choice(frontier)
            frontier.remove((x, y))

            neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]
            visited_neighbors = [n for n in neighbors if 0 <= n[1] < height and 0 <= n[0] < width and maze[n[1], n[0]]]

            if len(visited_neighbors) == 1:
                visited_x, visited_y = visited_neighbors[0]

                if 0 <= y < height and 0 <= x < width:  # Add the bounds check
                    maze[y, x] = True

                if 0 <= (y + visited_y) // 2 < height and 0 <= (x + visited_x) // 2 < width:  # Add the bounds check
                    maze[(y + visited_y) // 2, (x + visited_x) // 2] = True

                for nx, ny in neighbors:
                    if 0 <= ny < height and 0 <= nx < width and not maze[ny, nx] and (nx, ny) not in frontier:
                        frontier.append((nx, ny))

        return maze

    def find_farthest_points(self, maze):
        grid = Grid(matrix=maze.astype(int))

        # Find a random open space in the maze
        open_spaces = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell]
        start = random.choice(open_spaces)

        # Perform BFS search to find the farthest point from the start
        farthest_point, max_distance = self.bfs(maze, grid, start)

        # Find all points with the max distance
        farthest_points = [point for point in open_spaces if self.bfs(maze, grid, start)[1] < max_distance]

        # Choose a random farthest point
        farthest_point2 = random.choice(farthest_points)

        return farthest_point, farthest_point2

    def bfs(self, maze, grid, start):
        start_node = grid.node(*start)
        finder = BreadthFirstFinder()
        max_distance = 0
        farthest_point = start

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell:
                    end_node = grid.node(x, y)
                    path, _ = finder.find_path(start_node, end_node, grid)
                    if len(path) - 1 > max_distance:
                        max_distance = len(path) - 1
                        farthest_point = (x, y)

        return farthest_point, max_distance

    def generate(self):
        grid = self.generate_maze(self.width, self.height)
        level = [['W' if cell else ' ' for cell in row] for row in grid.tolist()]
        level = self.add_start_and_end(level, grid)
        level = self.add_obstacles_and_quarks(level)
        return level

    def add_obstacles_and_quarks(self, level):
        for y, row in enumerate(level):
            for x, cell in enumerate(row):
                if cell == ' ':  # Empty space
                    if random.random() < 0.05:  # 5% chance of placing a quark
                        level[y][x] = 'Q'
        return level

    def add_start_and_end(self, level_data, occupancy_grid):
        start, end = self.find_farthest_points(occupancy_grid)
        level_data[start[1]][start[0]] = 'S'
        level_data[end[1]][end[0]] = 'E'
        self.start, self.end = start, end
        return level_data

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])