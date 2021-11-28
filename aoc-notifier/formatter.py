import datetime

import inflect

INFLECT = inflect.engine()


def format_leaderboard_changes(leaderboard_changes):
    result = ""
    for change in leaderboard_changes:
        result += f"{':arrow_up:' if change['positive'] else ':arrow_down:'} *{INFLECT.ordinal(change['position'])}* {change['username']} ({change['points']} points)\n"

    return result


def format_complete_chal_message(challenge):
    star = ":star2:" if challenge["part"] == 2 else ":star:"
    timestamp = datetime.datetime.fromtimestamp(challenge['timestamp'])

    return f"*{challenge['username']}* has completed {star} *Day {challenge['day']}* ({challenge['part']}) at {timestamp.strftime('%H:%M:%S')}!"


def format_changes(challenge_changes, leaderboard_changes):
    pass
