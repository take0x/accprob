import subprocess
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By


def main() -> None:
    url = input("URL: ")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    time.sleep(3)

    contest_title = driver.find_element(By.XPATH, "//h1").text
    links = driver.find_elements(By.XPATH, "//table//td/a")

    for index, link in enumerate(links, start=1):
        if (href := link.get_attribute("href")) is None:
            print(f"Failed to download the test case: {index:02}")
            sys.exit(1)

        contest_id = href.split("/")[-3]
        problem_id = href.split("/")[-1]
        problem_dir = contest_title + "/" + format(index, "02") + "/test"
        problem_url = f"https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}"
        command = ["oj", "d", "-d", problem_dir, problem_url]
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            check=True,
        )
        print(f"Downloaded the test case: {index:02} {problem_id}")

    driver.close()


if __name__ == "__main__":
    main()
