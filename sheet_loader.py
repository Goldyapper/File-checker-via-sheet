import pandas as pd


XLSX_PATH   = "Doctor Who Timeline.xlsx"

SKIP_SHEETS = [
    "Time war",
    "Time Lord Victorious",
    "Daleks",
]


def get_sheet_names(xlsx_path):
    xl = pd.ExcelFile(xlsx_path)
    sheets = xl.sheet_names[9:10]
    return [s for s in sheets if s not in SKIP_SHEETS]

SHEET_NAMES =  get_sheet_names(XLSX_PATH)


def season_sort_key(sn):
    if sn.startswith("FS"):
        # FS seasons sort after all regular seasons, preserving order
        rest = sn[2:].strip()
        try:
            return (2, int(rest), 0)
        except ValueError:
            return (2, 99, 0)
        
    elif sn.startswith("S"):
        rest = sn[1:].strip()
        try:
            return (1, int(rest), 0)
        except ValueError:
            return (1, 99, 0)
    return (3, 99, 0)

def load_stories(sheet_name,XLSX_PATH):
    df = pd.read_excel(XLSX_PATH, sheet_name=sheet_name, header=0)
    df.columns = range(len(df.columns))

    rows = []
    for _, r in df.iterrows():
        story   = str(r[0]).strip()
        timeline_season   = str(r[1]).strip()
        timeline_episode   = r[2]
        era     = str(r[3]).strip()
        watched_raw = r[4]
        series  = str(r[6]).strip()
        boxset  = str(r[7]).strip()
        episode = str(r[8]).strip()

        if (story in ("nan","") or timeline_season in ("nan","") or
                pd.isna(timeline_episode) or timeline_season.startswith("Season")):
            continue
        try:
            ep_num = int(float(timeline_episode))
        except (ValueError, TypeError):
            continue

        watched = (not pd.isna(watched_raw)) and float(watched_raw) == 1

        rows.append({
            "story": story,
            "timeline_season": timeline_season,
            "timeline_episode": ep_num,
            "era": era,
            "watched": watched,
            "series": series,
            "boxset": boxset,
            "episode": episode,
        })

    rows.sort(key=lambda r: (*season_sort_key(r["timeline_season"]), r["timeline_episode"]))    
    
    return rows

def sheet_loader():
    datasets = {}
    for name in SHEET_NAMES:
        print(f"{name} timeline scanned")
        stories = load_stories(name, XLSX_PATH)
        unwatched = [s for s in stories if not s["watched"]]
        datasets[name] = unwatched

        #print(f"{len(unwatched)} not watched")
        #for s in unwatched:
            #print(f"    {s['story']} - {s['timeline_season']}E{s['timeline_episode']}")

    return datasets