# Import necessary functions and classes from Intelligence.py
from Intelligence import evolve, Worm, food, mlp_2h, evaluate_fitness, tournament_selection, crossover, mutate
from Module import *
import numpy as np
from PIL import Image

# Define constants
population_size = 5
generations = 20
mutation_rate = 0.05
mutation_strength = 0.1
elite_size = 2

# Initialize the population globally
population = [mlp_2h(10, 10, 10, 4, 0.01, 1) for _ in range(population_size)]

# Test
def save_best_individual_actions(individual):
    """Simulate the best individual and save its actions as PNG images."""
    global W1, F1, F2, End
    W1 = Worm(3, 3)
    F1 = food(5, 4)
    F2 = food(10, 10)
    F1.placement()
    F2.placement()

    # Reset worm history
    W1.historyy = [W1.pointy] * W1.length
    W1.historyx = [W1.pointx] * W1.length

    # Reset End variable
    End = False

    for step in range(100):  # Run for a fixed number of steps
        if End:
            print("Simulation ended due to invalid state.")
            break

        input_datas = np.array([
            W1.pointy,  # Worm's Y position
            W1.pointx,  # Worm's X position
            F1.pointyf,  # Food 1 Y position
            F1.pointxf,  # Food 1 X position
            F2.pointyf,  # Food 2 Y position
            F2.pointxf,  # Food 2 X position
            int(W1.facing == "north"),  # One-hot encoding for direction
            int(W1.facing == "south"),
            int(W1.facing == "west"),
            int(W1.facing == "east")
        ])
        _, _, output = individual.forward(input_datas)

        move_direction = np.argmax(output)  # Choose action
        if move_direction == 0:
            W1.moving("u")
        elif move_direction == 1:
            W1.moving("d")
        elif move_direction == 2:
            W1.moving("l")
        elif move_direction == 3:
            W1.moving("r")

        # Check if the worm is out of bounds
        if W1.pointx < 0 or W1.pointx > 19 or W1.pointy < 0 or W1.pointy > 19:
            End = True
            print(f"Worm died: Out of bounds at ({W1.pointx}, {W1.pointy})")
            break

        W1.drawing()

        # Debug the place array
        print(np.array(place))  # Print the grid to verify food placement

        # Save the current state as a PNG image
        array = np.array(place, dtype=np.uint8) * 255
        img = Image.fromarray(array, mode='L')
        img.save(f"Final_Generation_Step_{step}.png")
        print(place)  # Print the grid to verify its values

def evolve():
    """Evolve the population using genetic algorithms."""
    global population
    for gen in range(generations):
        print(f"\n=== Generation {gen} ===")

        # Evaluate fitness
        fitness_scores = [evaluate_fitness(individual) for individual in population]

        # Sort by fitness
        sorted_pop = [x for _, x in sorted(zip(fitness_scores, population), key=lambda pair: -pair[0])]

        best_fitness = fitness_scores[np.argmax(fitness_scores)]
        print(f"Best fitness: {best_fitness}")

        # Elitism
        new_population = sorted_pop[:elite_size]

        # Generate new population
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)

            child_genome = crossover(parent1.to_genome(), parent2.to_genome())
            child_genome = mutate(child_genome, mutation_rate, mutation_strength)

            child_net = mlp_2h.from_genome(
                child_genome,
                input_size=10,
                hidden1_size=10,
                hidden2_size=10,
                output_size=4
            )
            new_population.append(child_net)

        population = new_population

    # Save the actions of the best individual in the final generation
    best_individual = sorted_pop[0]
    save_best_individual_actions(best_individual)



# === Main Execution ===
if __name__ == "__main__":
    # Run the evolution process
    evolve()
