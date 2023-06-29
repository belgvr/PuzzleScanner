# Bitcoin Puzzle Solver

This Python script solves Bitcoin puzzles by searching for matching Bitcoin addresses within a given range. It supports two scanning modes: random scanning and incremental scanning.

## Dependencies

To run this script, you need the following dependencies:

- Python 3.x
- The `bitcoin` library (can be installed via pip: `pip install bitcoin`)

## Usage

1. Clone the repository or download the `bitcoin_puzzle_solver.py` file.
2. Install the required dependencies as mentioned above.
3. Open a terminal or command prompt.
4. Navigate to the directory containing the script.
5. Run the script with the following command:

`python bitcoin_puzzle_solver.py -p <puzzle_id> -m <mode>`

Replace `<puzzle_id>` with the ID of the Bitcoin puzzle you want to solve (1 to 10). Replace `<mode>` with the scan mode: `0` for random scanning or `1` for incremental scanning.
For example, to solve puzzle 1 using random scanning, run:

`python bitcoin_puzzle_solver.py -p 1 -m 0`


6. The script will start scanning for matching Bitcoin addresses within the specified range. The progress will be displayed in the terminal.
7. If a match is found, the script will display the private key, the compressed Bitcoin address, and create a file named `FOUND_<target_address>.txt` with the match details.

![image](https://github.com/belgvr/PuzzleScanner/assets/31529658/1531ab90-f9cc-4010-9fe0-27ba56187177)


## How It Works

1. The script takes a puzzle ID and scan mode as command-line arguments.
2. It defines a dictionary of puzzles with their corresponding details (target address, lower limit, and upper limit).
3. The script retrieves the puzzle details based on the provided ID.
4. It converts the lower and upper limits from hexadecimal to decimal.
5. Depending on the scan mode:
- For random scanning: The script generates random hexadecimal values within the specified range and checks if the corresponding Bitcoin address matches the target address.
- For incremental scanning: The script iterates through each value within the specified range, converts it to hexadecimal, and checks for a match.
6. When a match is found, the script displays the match details, creates a file with the match information, and terminates.

Feel free to explore and modify the code to suit your needs.

<!--## License

This project is licensed under the [MIT License](LICENSE).-->
