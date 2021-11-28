import json
import requests
import json


def get_leaderboard(id, session):
    response = requests.get(
        f"https://adventofcode.com/2021/leaderboard/private/view/{id}.json", headers={"cookie": f"session={session}"})
    if response.status_code != 200:
        raise ValueError(
            f"Request to AOC returned an error {response.status_code}, the response is:\n{response.text}"
        )
    return response.json()


def read_old_leaderboard(leaderboard_location):
    with open(leaderboard_location, 'r') as f:
        return json.load(f)


def write_old_leaderboard(leaderboard, location):
    with open(location, 'w+') as f:
        return json.dump(leaderboard, f)


def extract_changes(old_leaderboard, new_leaderboard):
    challenge_changes = collect_challenge_changes(
        old_leaderboard, new_leaderboard)
    leaderboard_changes = collect_leaderboard_changes(
        old_leaderboard, new_leaderboard)
    return (challenge_changes, leaderboard_changes)


def collect_challenge_changes(old_leaderboard, new_leaderboard):
    changes = []
    for (id, member) in new_leaderboard['members'].items():
        if id not in old_leaderboard['members']:
            continue
        old_member = old_leaderboard['members'][id]
        for (day, chal) in member['completion_day_level'].items():
            for (part, part_details) in chal.items():
                if day in old_member['completion_day_level'] and part in old_member['completion_day_level'][day]:
                    continue
                changes.append({
                    'username': member['name'],
                    'day': int(day),
                    'part': int(part),
                    'timestamp': int(part_details['get_star_ts'])
                })

    return sorted(changes, key=lambda x: x['timestamp'])


def collect_leaderboard_changes(old_leaderboard, new_leaderboard):
    changes = []
    old_positions = create_positions(old_leaderboard)
    new_positions = create_positions(new_leaderboard)
    for (id, new_info) in new_positions.items():
        if not id in old_positions:
            continue

        old_info = old_positions[id]
        if old_info['position'] == new_info['position']:
            continue

        changes.append({
            'username': new_info['username'],
            'position': new_info['position'],
            'points': new_info['points'],
            'positive': old_info['position'] > new_info['position']
        })
    return sorted(changes, key=lambda x: x['position'])


def create_positions(leaderboard):
    positions = {}
    position = 1
    for (id, member) in sorted(leaderboard['members'].items(), key=lambda x: (-x[1]['local_score'], int(x[1]['id']))):
        positions[id] = {
            'username': member['name'],
            'position': position,
            'points': member['local_score']
        }
        position += 1

    return positions
