from config import SEQUENCE_LENGTH


# Check if there is a sequence of identical characters in the specified direction
def has_sequence(dna, row, col, row_step, col_step):
    initial_char = dna[row][col]

    for i in range(1, SEQUENCE_LENGTH):
        new_row, new_col = row + i * row_step, col + i * col_step

        if (
            new_row >= len(dna)
            or new_col >= len(dna)
            or dna[new_row][new_col] != initial_char
        ):
            return False

    return True
