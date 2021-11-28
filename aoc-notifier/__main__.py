import os
import sys

from .leaderboard import *
from .webhook import *

OLD_LEADERBOARD = 'old_leaderboard.json'


session = os.environ['AOC_SESSION']
board_id = os.environ['AOC_BOARD']
slack_hook = os.environ.get('AOC_SLACK_HOOK')
discord_hook = os.environ.get('AOC_DISCORD_HOOK')

new_leaderboard = get_leaderboard(board_id, session)
try:
    old_leaderboard = read_old_leaderboard(OLD_LEADERBOARD)
except:
    print("No old leaderboard found, saving new leaderboard and quitting.")
    write_old_leaderboard(new_leaderboard, OLD_LEADERBOARD)
    sys.exit(1)

write_old_leaderboard(new_leaderboard, OLD_LEADERBOARD)
(challenge_changes, leaderboard_changes) = extract_changes(
    old_leaderboard, new_leaderboard)
if challenge_changes:
    print("Found changes! Informing webhooks")
    formatted_changes = format_changes(
        challenge_changes, leaderboard_changes, board_id)
    if slack_hook:
        send_slack_message(slack_hook, formatted_changes)
    if discord_hook:
        send_discord_message(discord_hook, formatted_changes)
