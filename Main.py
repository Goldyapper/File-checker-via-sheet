from audio_checker import check_stories,print_misplaced,print_missing

def main():
    missing, misplaced = check_stories()
    print_missing(missing)
    print_misplaced(misplaced)


if __name__ == "__main__":
    main()
    print("Done")