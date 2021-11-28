import os

from .leaderboard import *
from .webhook import *

OLD_LEADERBOARD = 'old_leaderboard.json'


def run_changes(board_id, session, slack_hook):
    new_leaderboard = get_leaderboard(board_id, session)
    try:
        old_leaderboard = read_old_leaderboard(OLD_LEADERBOARD)
    except:
        print("No old leaderboard found, saving new leaderboard and quitting.")
        write_old_leaderboard(new_leaderboard, OLD_LEADERBOARD)
        return
    write_old_leaderboard(new_leaderboard, OLD_LEADERBOARD)
    (challenge_changes, leaderboard_changes) = extract_changes(
        old_leaderboard, new_leaderboard)
    if challenge_changes:
        send_message(slack_hook, challenge_changes,
                     leaderboard_changes, board_id)


session = os.environ['AOC_SESSION']
aoc_board_id = os.environ['AOC_BOARD']
slack_webhook = os.environ['AOC_SLACK_HOOK']

run_changes(aoc_board_id, session, slack_webhook)
