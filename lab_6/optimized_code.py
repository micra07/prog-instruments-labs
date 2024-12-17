import json
import math
import os
import logging
from scipy.special import erfc
from mpmath import gammainc
from constants import PATH, M, P_I

def read_json_file(filename: str) -> dict:
    """
    Reads a JSON file and returns the data as a dictionary.

    Parameters: 
    The name of the JSON file to read.

    Returns: 
    A dictionary containing the data read from the JSON file.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Error reading file {filename}: {e}")
        return {}

def frequency_bitwise_test(sequence: str) -> float:
    """
    Performs a frequency bitwise test.

    Parameters: 
    The binary sequence to test.

    Returns: 
    The P-value calculated by the statistical test.
    """
    try:
        N = len(sequence)
        sum = sequence.count("1") - sequence.count("0")
        S_N = abs(sum) / math.sqrt(N)
        P_value = erfc(S_N / math.sqrt(2))
        if P_value < 0 or P_value > 1:
            raise ValueError('Error: P should be in range [0, 1]')
        return P_value
    except Exception as e:
        print(f"Error: {e}")
        raise


def similar_sequences_test(sequence: str) -> float:
    """
    Performs a test for the same consecutive bits.
    
    Parameters:
    The binary sequence to test.
    
    Returns:
    The P-value calculated by the statistical test.
    """
    try:
        N = len(sequence)
        sum_of_ones = sequence.count("1")
        proportion_of_ones = sum_of_ones / N
        if abs(proportion_of_ones - 0.5) >= 2 / math.sqrt(N):
            return 0

        transitions = sum(1 for i in range(N - 1) if sequence[i] != sequence[i + 1])
        term = 2 * N * proportion_of_ones * (1 - proportion_of_ones)
        deviation = abs(transitions - term)
        P_value = erfc(deviation / (2 / math.sqrt(2 * N) * term))
        if P_value < 0 or P_value > 1:
            raise ValueError('Error: P should be in range [0, 1]')
        return P_value
    except Exception as e:
        print(f"Error: {e}")
        raise


def longest_ones_sequence_test(sequence: str) -> float:
    """
    Performs a test for the longest sequence of units in the block.
    
    Parameters:
    The binary sequence to test..
    
    Returns:
    The P-value calculated by the statistical test.
    """
    try:
        block_size = M
        blocks = (sequence[i:i + block_size] for i in range(0, len(sequence), block_size))
        V = [0] * 4

        for block in blocks:
            max_length = max((len(s) for s in block.split("0")), default=0)
            if max_length <= 1:
                V[0] += 1
            elif max_length == 2:
                V[1] += 1
            elif max_length == 3:
                V[2] += 1
            else:
                V[3] += 1

        Xi_2 = sum((V[i] - 16 * P_I[i]) ** 2 / (16 * P_I[i]) for i in range(4))
        P_value = gammainc(1.5, Xi_2 / 2)
        if P_value < 0 or P_value > 1:
            raise ValueError('Error: P should be in range [0, 1]')
        return P_value
    except Exception as e:
        print(f"Error: {e}")
        raise

def main() -> None:
    """
    Main function for output of results.
    """
    absolute_path = os.path.abspath(os.getcwd())
    json_data = read_json_file(absolute_path + PATH)
    if json_data:
        cpp_sequence = json_data.get("cpp_generator", "")
        java_sequence = json_data.get("java_generator", "")
    if cpp_sequence and java_sequence:
        print("Tests for cpp_sequence:")
        print("Frequency bitwise test: P = " + str(frequency_bitwise_test(cpp_sequence)))
        print("Similar sequences test: P = " + str(similar_sequences_test(cpp_sequence)))
        print("Longest ones sequence test: P = " + str(longest_ones_sequence_test(cpp_sequence)))
        print("Tests for java_sequence:")
        print("Frequency bitwise test: P = " + str(frequency_bitwise_test(java_sequence)))
        print("Similar sequences test: P = " + str(similar_sequences_test(java_sequence)))
        print("Longest ones sequence test: P = " + str(longest_ones_sequence_test(java_sequence)))

if __name__ == "__main__":
    main()
