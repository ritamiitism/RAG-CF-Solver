import requests


def is_contest_running(contest_id):

    url = "https://codeforces.com/api/contest.list"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "OK":
        return False

    contests = data["result"]

    for contest in contests:

        if contest["id"] == contest_id:

            phase = contest["phase"]

            if phase == "CODING":
                return True

            return False

    return False


# ---------------- TEST ---------------- #
if __name__ == "__main__":

    contest_id = 71

    print(is_contest_running(contest_id))