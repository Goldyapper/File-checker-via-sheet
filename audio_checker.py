from sheet_loader import sheet_loader
from file_loader import file_loader
from utils import normaliser, extract_digits


def check_stories():
    sheet_data = sheet_loader()
    file_data = file_loader()

    file_index = {}
    for f in file_data:
        file_index.setdefault(normaliser(f["name"]), []).append(f)

    missing = []
    misplaced = []
    for sheet_name, stories in sheet_data.items():
        for story in stories:
            key = normaliser(story["story"])
            matches = file_index.get(key)

            if not matches:
                if not story["watched"]:
                    missing.append({
                        "sheet": sheet_name,
                        "story": story["story"],
                        "timeline_season": story["timeline_season"],
                        "timeline_episode": story["timeline_episode"],
                        "series": story["series"],
                        "boxset": story["boxset"],
                        "episode": story["episode"],
                    })
                continue

            expected_season = extract_digits(story["timeline_season"])
            expected_episode = story["timeline_episode"]

            for f in matches:
                actual_season = extract_digits(f["season"])
                actual_episode = extract_digits(f["episode_number"])

                if expected_season != actual_season or expected_episode != actual_episode:
                    misplaced.append({
                        "sheet": sheet_name,
                        "story": story["story"],
                        "expected_season": story["timeline_season"],
                        "expected_episode": story["timeline_episode"],
                        "actual_season": f["season"],
                        "actual_episode": f["episode_number"],
                        "actual_doctor": f.get("doctor", ""),
                    })

    return missing, misplaced

def print_missing(missing):
    print(f"\n{len(missing)} unwatched stories not found in the folders:")

    last_sheet = None
    last_season = None
    for m in missing:
        if m["sheet"] != last_sheet:
            print(f"\n=== {m['sheet']} ===")
            last_sheet = m["sheet"]
            last_season = None
        if m["timeline_season"] != last_season:
            print(f"  -- {m['timeline_season']} --")
            last_season = m["timeline_season"]
        print(f"    {m['story']} - {m['timeline_season']}E{m['timeline_episode']}  "
            f"({m['series']} / {m['boxset']} / {m['episode']})")

def print_misplaced(misplaced):
    print(f"\n{len(misplaced)} stories found but need to be moved:")

    last_sheet = None
    last_season = None
    for m in misplaced:
        if m["sheet"] != last_sheet:
            print(f"\n=== {m['sheet']} ===")
            last_sheet = m["sheet"]
        if m["expected_season"] != last_season:
            print(f"  -- {m['expected_season']} --")
            last_season = m["expected_season"]
        print(f"    {m['story']}: currently S{m['actual_season']}E{m['actual_episode']}->  should be {m['expected_season']}E{m['expected_episode']}")