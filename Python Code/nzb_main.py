from nzb_search import nzb_search_helper

def main():
    print("<< MAIN START >>")
    cls = nzb_search_helper()
    cls.select_all_movies()
    print("<< MAIN END >>")

if __name__ == '__main__':
    main()