import pandas as pd
import logging

# Set up logging with colors
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# Helper function for logging with colors
def log_result(message, is_win):
    color = '\033[92m' if is_win else '\033[91m'  # Green if win, red if lose
    logger.info(f"{color}{message}\033[0m")

# Function to analyze a match
def analyze_match(row):
    try:
        home_odds = row['B365H']
        draw_odds = row['B365D']
        away_odds = row['B365A']
    except KeyError:
        logger.error(f"Column names do not match expected names in file. Available columns: {list(row.index)}")
        return 0, 0, False

    outcome = row['FTR']
    profit = 0
    loss = 0
    bet_on_underdog_win_or_draw = False

    # Bet on underdog to win or draw
    if home_odds > 8 or draw_odds > 8 or away_odds > 8:
        if home_odds > 8 and (outcome == 'H' or outcome == 'D'):
            profit = home_odds - 1 if outcome == 'H' else draw_odds - 1
            bet_on_underdog_win_or_draw = True
        elif draw_odds > 8 and outcome == 'D':
            profit = draw_odds - 1
            bet_on_underdog_win_or_draw = True
        elif away_odds > 8 and (outcome == 'A' or outcome == 'D'):
            profit = away_odds - 1 if outcome == 'A' else draw_odds - 1
            bet_on_underdog_win_or_draw = True
        else:
            loss = -1  # Lose 1 unit because the underdog didn't win or draw
            bet_on_underdog_win_or_draw = True  # Count this match as analyzed even if lost

        log_result(f"Date: {row['Date']} - Match: {row['HomeTeam']} vs {row['AwayTeam']} - "
                   f"Odds: {max(home_odds, draw_odds, away_odds):.2f} - Outcome: {outcome} - "
                   f"P/L: {profit + loss:.2f}", profit > 0)

    return profit, loss, bet_on_underdog_win_or_draw

# Function to calculate total profit/loss for a single file
def calculate_profit_loss(file_name):
    df = pd.read_csv(file_name)
    total_matches = len(df)  # Total number of matches in the file
    df[['profit', 'loss', 'bet_made']] = df.apply(lambda row: analyze_match(row), axis=1, result_type='expand')
    total_profit = df['profit'].sum()
    total_loss = df['loss'].sum()
    balance = total_profit + total_loss
    matches_analyzed = df['bet_made'].sum()  # Count only the matches where a bet was made
    return balance, total_matches, matches_analyzed

# List of files to process
file_names = [
    'england-premier-league-2019-to-2020.csv',
    'england-premier-league-2018-to-2019.csv',
    'belgium-jupiler-league-2019-to-2020.csv',
    'germany-bundesliga-1-2019-to-2020.csv',
    'portugal-liga-i-2019-to-2020.csv',
    'italy-serie-a-2019-to-2020.csv',
    'france-le-championnat-2019-to-2020.csv',
    'netherlands-eredivisie-2019-to-2020.csv',
    'spain-la-liga-primera-division-2019-to-2020.csv',
]

# Main function to process all files and calculate the total balance
def main():
    total_balance = 0
    total_matches_analyzed = 0
    total_matches_in_files = 0
    for file_name in file_names:
        logger.info(f"\033[96m{'-'*20}\nAnalyzing file: {file_name}\033[0m")
        file_balance, total_matches, matches_analyzed = calculate_profit_loss(file_name)
        total_balance += file_balance
        total_matches_in_files += total_matches
        total_matches_analyzed += matches_analyzed
        logger.info(f"\033[96mBalance for {file_name}: {file_balance:.2f}\033[0m")
        logger.info(f"\033[96mTotal matches in {file_name}: {total_matches}\033[0m")
        logger.info(f"\033[96mTotal matches analyzed in {file_name}: {matches_analyzed}\033[0m")
    
    logger.info(f"\033[93mTotal Profit/Loss across all files: {total_balance:.2f}\033[0m")
    logger.info(f"\033[93mTotal matches in all files: {total_matches_in_files}\033[0m")
    logger.info(f"\033[93mTotal matches analyzed across all files: {total_matches_analyzed}\033[0m")

if __name__ == '__main__':
    main()

