from util import fetch_finviz

if __name__ == "__main__":
    data = fetch_finviz("META")
    for row in data:
        print(row)