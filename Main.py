import re

from sheet_loader import sheet_loader
from file_loader import file_loader

def normaliser(name):
    return re.sub(r'\s+', ' ', name).strip().lower()

def find_missing_audios():
    sheet_data = sheet_loader()
    file_data = file_loader()

    have_names = {normaliser(f["name"]) for f in file_data}

    missing = []
    for sheet_name, stories in sheet_data.items():
        for story in stories:
            if story["watched"]:
                continue
            if normaliser(story["story"]) not in have_names:
                missing.append({
                    "sheet": sheet_name,
                    "story": story["story"],
                    "timeline_season": story["timeline_season"],
                    "timeline_episode": story["timeline_episode"],
                })

    return missing



def main():
    missing = find_missing_audios()
    print(f"\n{len(missing)} unwatched stories not found in the input folder:")

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
        print(f"    {m['story']} - {m['timeline_season']}E{m['timeline_episode']}")


if __name__ == "__main__":
    main()
    print("Done")