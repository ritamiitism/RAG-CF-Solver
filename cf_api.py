import requests


def get_problem_metadata(contest_id, index):

    url = "https://codeforces.com/api/problemset.problems"

    response = requests.get(url)

    data = response.json()

    if data["status"] != "OK":
        return None

    problems = data["result"]["problems"]

    for problem in problems:

        if (
            problem.get("contestId") == contest_id
            and problem.get("index") == index
        ):

            return {
                "name": problem.get("name"),
                "rating": problem.get("rating"),
                "tags": problem.get("tags")
            }

    return None


# ---------------- TEST ---------------- #
if __name__ == "__main__":

    contest_id = 71
    index = "A"

    result = get_problem_metadata(contest_id, index)

    print(result)