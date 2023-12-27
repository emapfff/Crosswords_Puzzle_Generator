from random import randint, random, choice
import time
import os
GRID_SIZE = 20  # Size of the grid
HORIZONTAL = 0  # Constant representing horizontal direction
VERTICAL = 1    # Constant representing vertical direction
POPULATION_SIZE = 40  # Number of individuals in the population


class Word:
    def __init__(self, x0, y0, direction, word):
        # Constructor for the Word class, initializes a word instance with its starting coordinates,
        # direction, and the actual word.
        self.word = word  # The actual word
        self.x0 = x0  # Starting x-coordinate
        self.y0 = y0  # Starting y-coordinate
        self.direction = direction  # Direction of the word (HORIZONTAL or VERTICAL)
        self.x = self.calculate_end_coordinate_x()  # Ending x-coordinate
        self.y = self.calculate_end_coordinate_y()  # Ending y-coordinate

    def calculate_end_coordinate_x(self):
        # Calculate the x-coordinate of the end of the word based on its direction.
        # For horizontal words, it's the starting x-coordinate plus the length of the word minus 1.
        # For vertical words, it's the same as the starting x-coordinate.
        if self.direction == HORIZONTAL:
            return self.x0 + len(self.word) - 1
        else:
            return self.x0

    def calculate_end_coordinate_y(self):
        # Calculate the y-coordinate of the end of the word based on its direction.
        # For vertical words, it's the starting y-coordinate plus the length of the word minus 1.
        # For horizontal words, it's the same as the starting y-coordinate.
        if self.direction == VERTICAL:
            return self.y0 + len(self.word) - 1
        else:
            return self.y0


class Puzzle:
    def __init__(self, words_list: list[Word]):
        # Constructor for the Puzzle class, initializes a puzzle instance with a list of Word instances.
        self.words = words_list
        self.fitness_value = self.fitness()

    def get_fitness(self):
        # Get the fitness value of the puzzle.
        return self.fitness_value

    def print_puzzle(self):
        # Print the puzzle configuration.
        table = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Place words in the table based on their coordinates and direction.
        for word in self.words:
            x0, y0, x, y = word.x0, word.y0, word.x, word.y
            if x0 == x:
                count = 0
                for i in range(y0, y + 1):
                    # Fill in the table with characters from the word on the horizontal direction
                    table[i][x0] = word.word[count]
                    count += 1
            elif y0 == y:
                count = 0
                for j in range(x0, x + 1):
                    # Fill in the table with characters from the word on the vertical direction
                    table[y0][j] = word.word[count]
                    count += 1

        # Print the final puzzle configuration.
        for i in range(0, GRID_SIZE):
            for j in range(0, GRID_SIZE):
                print(table[i][j], end=' ')
            print()

    def fitness(self: list[Word]):
        # Calculate the fitness value of the puzzle.
        error = 0
        # Initialize the table to represent the puzzle grid.
        table = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        # Loop through each word in the puzzle to check for errors in the placement.
        for word in self.words:
            x0, y0, x, y = word.x0, word.y0, word.x, word.y
            if x0 == x:
                count = 0
                for i in range(y0, y + 1):
                    # Check for errors in the placement of the character of the word in the table.
                    if table[i][x0] != '.' and table[i][x0] != word.word[count]:
                        error += 5
                    table[i][x0] = word.word[count]
                    count += 1
            elif y0 == y:
                count = 0
                for j in range(x0, x + 1):
                    # Check for errors in the placement of the character of the word in the table.
                    if table[y0][j] != '.' and table[y0][j] != word.word[count]:
                        error += 5
                    table[y0][j] = word.word[count]
                    count += 1

        # Check for errors related to the proximity of words and intersections.
        for word1 in self.words:
            flag = False
            # Get coordinates from word1
            x1, y1 = word1.x0, word1.y0
            for word2 in self.words:
                if word1.word != word2.word:
                    # Get coordinates from word2
                    x2, y2 = word2.x0, word2.y0
                    # Check that parallel horizontal/vertical words’ symbols shouldn’t be existing for neighbor
                    # rows/columns.
                    if word1.direction == word2.direction == VERTICAL:
                        if abs(x1 - x2) <= 1 and (
                                y2 - len(word1.word) <= y1 < y2 + len(word2.word) or y1 -
                                len(word2.word) - 1 <= y2 < y1 + len(word1.word)):
                            error += 50
                    elif word1.direction == word2.direction == HORIZONTAL:
                        if abs(y1 - y2) <= 1 and (
                                x2 - len(word1.word) - 1 <= x1 < x2 + len(word2.word) or x1 -
                                len(word2.word) - 1 <= x2 < x1 + len(word1.word)):
                            error += 50
                    else:
                        # Check that parallel 90 degrees horizontal/vertical words’ symbols shouldn’t be existing for
                        # neighbor rows/columns.
                        if word1.direction == HORIZONTAL:
                            if (x2 == x1 - 1 or x2 == x1 + len(word1.word)) and y2 <= y1 <= y2 + len(word2.word) - 1:
                                error += 25
                            if is_intersect([x1, y1], [x1 + len(word1.word) - 1, y1], [x2, y2],
                                            [x2, y2 + len(word2.word) - 1]):
                                flag = True
                        else:
                            if (y2 == y1 - 1 or y2 == y1 + len(word1.word)) and x2 <= x1 <= x2 + len(word2.word) - 1:
                                error += 25
                            if is_intersect([x1, y1], [x1, y1 + len(word1.word) - 1], [x2, y2],
                                            [x2 + len(word2.word) - 1, y2]):
                                flag = True
            if not flag:
                error += 12.5

        # Check for connected components in the table.
        k = 0
        visited = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if table[i][j] != '.' and not visited[i][j]:
                    dfs(table, visited, i, j)
                    k += 1
        error += (k - 1) * 100
        return error


def initial_genome(word_list):
    # Initialize an empty list to store Word objects representing the puzzle.
    tmp = []

    # Iterate over each word in the given list.
    for word in word_list:
        # Randomly choose the direction of the word, either HORIZONTAL or VERTICAL.
        direction = choice([HORIZONTAL, VERTICAL])

        # Based on the chosen direction, randomly select starting coordinates (x, y).
        if direction == HORIZONTAL:
            y = randint(0, GRID_SIZE - 1)
            x = randint(0, GRID_SIZE - len(word))
        else:
            x = randint(0, GRID_SIZE - 1)
            y = randint(0, GRID_SIZE - len(word))

        # Create a Word object with the chosen parameters and append it to the list.
        tmp.append(Word(x0=x, y0=y, direction=direction, word=word))

    # Return a Puzzle object containing the generated list of Word objects.
    return Puzzle(tmp)


def initial_population(word_list, population_size):
    # Initialize an empty list to store Puzzle objects representing the population.
    population = [initial_genome(word_list) for _ in range(population_size)]

    # Sort the population based on the fitness values of the puzzles.
    population.sort(key=lambda puzzle: puzzle.fitness_value)

    # Return the generated population.
    return population


def mutate(word_list: list[Word], mutation_rate=0.35):
    # Initialize an empty list to store mutated Word objects.
    mutated_population = []

    # Iterate through each Word object in the given list.
    for child in word_list:
        # Check if mutation should occur based on the mutation rate.
        if random() <= mutation_rate:
            # Randomly choose a new orientation (HORIZONTAL or VERTICAL).
            new_orientation = randint(0, 1)

            # Generate a new Word object with mutated properties.
            if new_orientation == HORIZONTAL:
                mutated_population.append(
                    Word(randint(0, GRID_SIZE - len(child.word)), randint(0, GRID_SIZE - 1), new_orientation,
                         child.word))
            else:
                mutated_population.append(
                    Word(randint(0, GRID_SIZE - 1), randint(0, GRID_SIZE - len(child.word)), new_orientation,
                         child.word))
        else:
            # If no mutation, add the unchanged Word object to the mutated population.
            mutated_population.append(child)

    # Return a Puzzle object created from the mutated population.
    return Puzzle(mutated_population)


def crossover(list_puzzles: list[Puzzle], probability=0.5):
    # Initialize an empty list to store the offspring Puzzles.
    temp = []
    # Iterate through pairs of Puzzles in the given list.
    for i in range(int(len(list_puzzles))):
        for j in range(i + 1, len(list_puzzles)):
            # Create copies of the words in the selected Puzzles.
            one_puzzle = list_puzzles[i].words.copy()
            two_puzzle = list_puzzles[j].words.copy()
            # Iterate through each word and perform crossover with a certain probability.
            new_child = []
            for k in range(len(one_puzzle)):
                if random() <= probability:
                    new_child.append(one_puzzle[k])
                else:
                    new_child.append(two_puzzle[k])
            # Add the mutated offspring Puzzles to the temporary list.
            temp.append(mutate(new_child))

    # Return the list of mutated offspring Puzzles.
    return temp


def on_segment(p, q, r):
    # Check if point q lies on the line segment between points p and r.
    if max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and max(p[1], r[1]) >= q[1] >= min(p[1], r[1]):
        return True
    return False


def orientation(p, q, r):
    # Determine the orientation of triplet (p, q, r).
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear points
    if val > 0:
        return 1  # Clockwise orientation
    else:
        return 2  # Counterclockwise orientation


def is_intersect(p1, q1, p2, q2):
    # Check if line segment (p1, q1) intersects with line segment (p2, q2).
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True  # General case of intersection

    # Special cases where segments are collinear and one segment lies on the other.
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False  # No intersection


def dfs(matrix, visited, x, y):
    # Depth-First Search (DFS) algorithm for traversing a 2D matrix.
    if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
        if matrix[x][y] != '.' and not visited[x][y]:
            visited[x][y] = True
            # Recursively explore neighbors in all four directions.
            dfs(matrix, visited, x + 1, y)
            dfs(matrix, visited, x - 1, y)
            dfs(matrix, visited, x, y + 1)
            dfs(matrix, visited, x, y - 1)


def main():
    path = "students/EmilDavlityarov/"
    output_path = f'{path}outputs'
    input_path = f'{path}inputs'
    os.mkdir(output_path)
    input_files = os.listdir(input_path)
    for file in input_files:
        # Read input file for the current test case
        file_path = f'{input_path}/{file}'
        words = []
        with open(file_path, 'r') as f:
            content = f.readlines()
        for line in content:
            words.append(line.strip())
        # Measure execution time and initialize population
        print(words)
        start_time = time.time()
        population = initial_population(words, POPULATION_SIZE)
        last_ans = -1
        count = 0
        # Evolution loop
        while population[0].fitness_value != 0:
            offspring = crossover(population)
            population += offspring
            population.sort(key=lambda x: x.fitness_value)
            population = population[:int(POPULATION_SIZE)]
            if last_ans == population[0].fitness_value:
                count += 1
            else:
                last_ans = population[0].fitness_value
                count = 0
            if count > 400:
                # Reset population if stuck
                population = initial_population(words, POPULATION_SIZE)
                count = 0
        # Write output to file
        file_out = f'output{file[5:-4]}'
        output_file_path = f'{output_path}/{file_out}'
        with open(output_file_path, 'w') as output_file:
            for a in population[0].words:
                output_line = f"{a.y0} {a.x0} {a.direction}\n"
                output_file.write(output_line)


if __name__ == "__main__":
    main()
