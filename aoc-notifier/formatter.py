import datetime
from dataclasses import dataclass

import inflect

INFLECT = inflect.engine()


@dataclass
class FormattedMessage:
    challenge_messages: list[str]
    leaderboard_messages: list[str]
    board_id: str


def format_challenge_message(challenge) -> str:
    star = ":star2:" if challenge["part"] == 2 else ":star:"
    timestamp = datetime.datetime.fromtimestamp(challenge['timestamp'])

    return f"*{challenge['username']}* has completed {star} *Day {challenge['day']}* ({challenge['part']}) at {timestamp.strftime('%H:%M:%S')}!"


def format_leaderboard_change(change) -> str:
    return f"{':arrow_up:' if change['positive'] else ':arrow_down:'} *{INFLECT.ordinal(change['position'])}* {change['username']} ({change['points']} points)\n"


def format_changes(challenge_changes, leaderboard_changes, board_id) -> FormattedMessage:
    FormattedMessage([format_challenge_message(change) for change in challenge_changes], [
                     format_leaderboard_change(change) for change in leaderboard_changes], board_id)
    pass
