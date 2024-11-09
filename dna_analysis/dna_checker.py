from dna_analysis.helpers import has_sequence
from constants import MIN_SEQUENCE_COUNT, SEQUENCE_LENGTH


def is_mutant(dna):
    grid_size = len(dna)
    mutation_count = 0

    # Check if the grid is small, no need to continue
    if grid_size < SEQUENCE_LENGTH:
        return False

    for row in range(grid_size):
        for col in range(grid_size):
            # Check horizontally
            if col + SEQUENCE_LENGTH <= grid_size and has_sequence(dna, row, col, 0, 1):
                mutation_count += 1

            # Check vertically
            if row + SEQUENCE_LENGTH <= grid_size and has_sequence(dna, row, col, 1, 0):
                mutation_count += 1

            # Check diagonally (down-right)
            if (
                row + SEQUENCE_LENGTH <= grid_size
                and col + SEQUENCE_LENGTH <= grid_size
                and has_sequence(dna, row, col, 1, 1)
            ):
                mutation_count += 1

            # Check if the minimum sequence count for mutants is met, no need to continue
            if mutation_count >= MIN_SEQUENCE_COUNT:
                return True

    return False
