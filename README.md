# Underdog Simulator

The `underdog_simulator.py` script simulates betting on underdog football teams' victories or draws across major European leagues during the 2005-2020 season. It analyzes the profitability of betting on matches where the odds of an underdog win or draw exceed 8.

## Prerequisites

To run the script, you need to install the required Python packages. Install them using the following command:

```bash
pip install -r requirements.txt
```

### Requirements

- `pandas`
- `logging`
- `xml.etree.ElementTree`
- `argparse`

## Usage

The script requires an XML file that contains the paths to the CSV files with match data. Each CSV file should include the following columns:

- `Date`
- `HomeTeam`
- `AwayTeam`
- `B365H` (Odds for home team win)
- `B365D` (Odds for draw)
- `B365A` (Odds for away team win)
- `FTR` (Full-time result: 'H' for home win, 'D' for draw, 'A' for away win)

### Run the Script

```bash
python underdog_simulator.py path/to/xml_file.xml
```

### Output

The script will output the following information:

- **Balance for each file**: The profit/loss balance calculated from bets placed on underdog victories or draws.
- **Total matches**: The number of matches in each file.
- **Total matches analyzed**: The number of matches where a bet was placed on the underdog.

### Example

```bash
python underdog_simulator.py matches.xml
```

This command will analyze the matches listed in `matches.xml`, displaying the profit/loss for each CSV file and a summary across all files.
