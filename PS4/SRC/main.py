import os
from utils import read_input_file, write_output_file
from algorithms import pl_resolution

def main():
    # Define input and output folders and number of test cases
    input_folder = 'input'
    output_folder = 'output'
    test_cases = 5
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each test case
    for i in range(1, test_cases + 1):
        input_file = os.path.join(input_folder, f"input0{i}.txt")
        output_file = os.path.join(output_folder, f"output0{i}.txt")
        
        # Read input file
        alpha, KB = read_input_file(input_file)
        
        # Perform PL resolution
        entails, steps = pl_resolution(KB, alpha)
        
        # Write output file
        write_output_file(output_file, steps, entails)

if __name__ == "__main__":
    main()