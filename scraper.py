
import requests
from bs4 import BeautifulSoup


def get_problem_statement(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        )
    }

    try:

        # STEP 1 -> Download webpage HTML
        response = requests.get(url, headers=headers)

        print("Status Code:", response.status_code)

        if response.status_code != 200:
            return "Failed to fetch webpage."

        # STEP 2 -> Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # STEP 3 -> Find problem statement div
        problem_div = soup.find("div", class_="problem-statement")

        if not problem_div:
            return "Problem statement not found."

        # STEP 4 -> Extract readable text
        text = problem_div.get_text(separator="\n")

        return text.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# ---------------- TEST ---------------- #
if __name__ == "__main__":

    url = "https://codeforces.com/problemset/problem/71/A"

    result = get_problem_statement(url)

    print(result[:3000])