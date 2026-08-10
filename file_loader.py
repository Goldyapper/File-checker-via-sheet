import os
import re
from config import mypath


def parse_file(file_path,season_folder):
    """Extract name + episode number from the filename, and season from the
    name of the folder the file sits in."""

    raw_name = os.path.splitext(os.path.basename(file_path))[0]

    # Expected filename format: "<episode number> - <name>"
    match = re.match(r'^\s*E?(\d+)\s*-\s*(.+)$', raw_name)
    if match:
        episode_number = match.group(1).strip()
        name = match.group(2).strip()
    else:
        episode_number = ''
        name = raw_name.strip()

    season_match = re.search(r'\d+', season_folder)
    if season_match:
        season = f"{int(season_match.group()):02d}"
    else:
        season = season_folder

    return {
        "name": name,
        "episode_number": episode_number,
        "season": season,
    }



def scan_audio_files(root_path):

    results = []
    for timeline_entry in sorted(os.scandir(root_path), key=lambda e: e.name):
        if not timeline_entry.is_dir():
            continue
        for season_entry in sorted(os.scandir(timeline_entry.path), key=lambda e: e.name):
            if not season_entry.is_dir():
                continue
            for item in sorted(os.scandir(season_entry.path), key=lambda e: e.name):
                if item.is_dir():
                    entry = parse_file(item.name, season_entry.name)
                elif item.is_file() and item.name.lower().endswith('.mp3'):
                    entry = parse_file(item.name, season_entry.name)
                else:
                    continue
                entry["timeline"] = timeline_entry.name
                results.append(entry)
    return results


def file_loader():
    return scan_audio_files(mypath)
