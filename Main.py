import pandas as pd
import os

from loader import load_stories, get_sheet_names

XLSX_PATH   = "Doctor Who Timeline.xlsx"

SHEET_NAMES =  get_sheet_names(XLSX_PATH)


def main():
    datasets = {}
    for name in SHEET_NAMES:
        print(f"{name}:")
        stories = load_stories(name, XLSX_PATH)
        datasets[name] = stories

        unwatched = [s for s in stories if not s["watched"]]
        print(f"{len(unwatched)} not watched")
        for s in unwatched:
            print(f"    {s['story']} - {s['timeline_season']}E{s['timeline_episode']}")


if __name__ == "__main__":
    main()
    print("Done")