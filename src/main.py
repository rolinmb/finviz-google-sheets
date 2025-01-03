from util import *
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("src/main.py : __main__ :: ERROR ::: Must enter one alphabetical command line argument for underlying ticker.")
        sys.exit(1)
    ticker = check_user_input(sys.argv[1])
    data_dict = fetch_finviz(ticker)
    upload_data_dict(data_dict)