from audio_checker import check_stories,print_misplaced,print_missing
from txt_writer import write_to_txt

def main():
    missing, misplaced = check_stories()
    #print_missing(missing)
    #print_misplaced(misplaced)
    write_to_txt(missing,misplaced)



if __name__ == "__main__":
    main()
    print("Done")