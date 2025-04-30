import sys
import collections
import heapq
from typing import List


def min_steps_to_collect_all_keys(maze: List[List[str]]) -> int:
    height, width = len(maze), len(maze[0])

    robots = []
    all_keys = {}
    key_count = 0

    for r in range(height):
        for c in range(width):
            cell = maze[r][c]
            if cell == '@':
                robots.append((r, c))
            elif 'a' <= cell <= 'z':
                all_keys[cell] = (r, c)
                key_count += 1

    if len(robots) == 1:
        r, c = robots[0]
        surrounding = [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1),
                       (r + 1, c + 1)]
        if all(0 <= nr < height and 0 <= nc < width and maze[nr][nc] == '@' for
               nr, nc in surrounding):
            maze[r][c] = '#'
            maze[r - 1][c] = '#'
            maze[r + 1][c] = '#'
            maze[r][c - 1] = '#'
            maze[r][c + 1] = '#'
            robots = surrounding

    paths = {}


    points_of_interest = robots + list(all_keys.values())

    for start_pos in points_of_interest:
        queue = collections.deque(
            [(start_pos, 0, 0)])
        visited = {start_pos: (0, 0)}

        while queue:
            pos, dist, doors = queue.popleft()
            r, c = pos

            cell = maze[r][c]
            if 'a' <= cell <= 'z' and pos != start_pos:
                key_bit = 1 << (ord(cell) - ord('a'))
                if start_pos not in paths:
                    paths[start_pos] = {}
                paths[start_pos][pos] = (dist, doors, key_bit)

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                new_pos = (nr, nc)

                if not (0 <= nr < height and 0 <= nc < width) or maze[nr][
                    nc] == '#':
                    continue

                new_doors = doors
                if 'A' <= maze[nr][nc] <= 'Z':
                    door_bit = 1 << (ord(maze[nr][nc]) - ord('A'))
                    new_doors |= door_bit

                if new_pos not in visited or visited[new_pos][1] > new_doors:
                    visited[new_pos] = (dist + 1, new_doors)
                    queue.append((new_pos, dist + 1, new_doors))

    all_keys_mask = (1 << key_count) - 1
    initial_state = (tuple(robots), 0)

    pq = [(0, initial_state)]
    visited_states = {initial_state: 0}

    while pq:
        steps, (robot_positions, keys_mask) = heapq.heappop(pq)

        if keys_mask == all_keys_mask:
            return steps


        if visited_states.get((robot_positions, keys_mask),
                              float('inf')) < steps:
            continue

        for robot_idx, robot_pos in enumerate(robot_positions):
            if robot_pos in paths:
                for target_pos, (dist, doors_mask, key_bit) in paths[
                    robot_pos].items():
                    if keys_mask & key_bit:
                        continue

                    if (doors_mask & ~keys_mask) == 0:
                        new_positions = list(robot_positions)
                        new_positions[robot_idx] = target_pos
                        new_positions = tuple(new_positions)

                        new_keys_mask = keys_mask | key_bit

                        new_state = (new_positions, new_keys_mask)
                        new_steps = steps + dist

                        if new_steps < visited_states.get(new_state,
                                                          float('inf')):
                            visited_states[new_state] = new_steps
                            heapq.heappush(pq, (new_steps, new_state))

    return -1


def get_input():
    return [list(line.strip()) for line in sys.stdin]


def solve(data):
    return min_steps_to_collect_all_keys(data)


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()