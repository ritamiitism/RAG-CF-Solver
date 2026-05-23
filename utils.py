def parse_codeforces_url(url):

    parts = url.strip().split("/")

    contest_id = int(parts[-2])
    index = parts[-1]

    return contest_id, index


# TEST
if __name__ == "__main__":

    url = "https://codeforces.com/problemset/problem/71/A"

    contest_id, index = parse_codeforces_url(url)

    print(contest_id)
    print(index)