from audio_checker import format_missing_lines, format_misplaced_lines

def write_to_txt(missing, misplaced, missing_path="missing.txt", misplaced_path="misplaced.txt"):
    """Write the missing and misplaced reports to two separate txt files."""
    with open(missing_path, "w", encoding="utf-8") as f:
        f.write("\n".join(format_missing_lines(missing)))

    with open(misplaced_path, "w", encoding="utf-8") as f:
        f.write("\n".join(format_misplaced_lines(misplaced)))

    print(f"Wrote {missing_path} and {misplaced_path}")
