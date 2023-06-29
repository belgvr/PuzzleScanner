# Bitcoin Puzzle Solver

This Python script solves Bitcoin puzzles by searching for matching Bitcoin addresses within a given range. It supports two scanning modes: random scanning and incremental scanning.
The logic behind this script is to systematically generate Bitcoin addresses within a given range and check if they match the target address of the puzzle. However, solving Bitcoin puzzles through exhaustive scanning like this can be incredibly time-consuming and impractical due to the colossal number of possible addresses. In fact, the chances of finding a match through this method alone are highly dependent on luck.
You might need an extraordinary stroke of luck to stumble upon the correct private key and address combination.
Therefore, while this script provides a starting point, it's crucial to explore alternative approaches such as GPU implementation or leveraging specialized hardware to significantly speed up the process. I'm open to new ideas and innovations to tackle these puzzles more efficiently and effectively!

## Dependencies

To run this script, you need the following dependencies:

- Python 3.x
- The `bitcoin` library (can be installed via pip: `pip install bitcoin`)

## Usage

1. Clone the repository or download the `bitcoin_puzzle_solver.py` file.

`git clone <repository_url>`

3. Install the required dependencies as mentioned above.

`pip install bitcoin`

4. Open a terminal or command prompt.
5. Navigate to the directory containing the script.
6. use `-h` argument to display this help:

~~~
Solve bitcoin puzzles.
Optional arguments:
  -h, --help  show this help message and exit
  -p P        Puzzle ID to attempt
  -m {0,1}    Scan mode: 0 for random, 1 for incremental
~~~

7. Run the script with the following command:

`python bitcoin_puzzle_solver.py -p <puzzle_id> -m <mode>`

Replace `<puzzle_id>` with the ID of the Bitcoin puzzle you want to solve (1 to 10). Replace `<mode>` with the scan mode: `0` for random scanning or `1` for incremental scanning.
For example, to solve puzzle 1 using incremental scanning, run:

`python bitcoin_puzzle_solver.py -p 1 -m 0`


8. The script will start scanning for matching Bitcoin addresses within the specified range. The progress will be displayed in the terminal.
9. If a match is found, the script will display the private key, the compressed Bitcoin address, and create a file named `FOUND_<target_address>.txt` with the match details.

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

## External reference
For more information about the puzzles, visit [https://privatekeys.pw/puzzles/bitcoin-puzzle-tx](https://privatekeys.pw/puzzles/bitcoin-puzzle-tx).

<!--## License

This project is licensed under the [MIT License](LICENSE).-->
