import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import TypeAlias, TypedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

Args: TypeAlias = argparse.Namespace

INFO_FILE = "contest-info.json"


class New:
    class Problem(TypedDict):
        contest_id: str
        problem_id: str
        url: str

    def __init__(self, url: str) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url)
        time.sleep(3)

        self.url = url
        self.problems: dict[int, New.Problem] = {}
        self.contest_title = self.driver.find_element(By.XPATH, "//h1").text
        self.links = self.get_links()

    def __del__(self) -> None:
        self.driver.close()

    def get_mode(self) -> str:
        label = self.driver.find_element(By.CLASS_NAME, "badge-secondary").text
        return label.split()[1]

    def get_links(self) -> list[WebElement]:
        mode = self.get_mode()

        match mode:
            case "Normal":
                value = "//td/a"
                return self.driver.find_elements(By.XPATH, value)
            case "Lockout":
                value = "//h3[@class='card-header']/a"
                return self.driver.find_elements(By.XPATH, value)
            case "Training":
                first_progress = self.driver.find_element(By.XPATH, "//table//td[a]")
                return first_progress.find_elements(By.XPATH, "a")
            case _ as unreachable:
                raise AssertionError(unreachable)

    def create_info(self) -> None:
        path = Path(self.contest_title, INFO_FILE)

        with path.open("w") as f:
            json.dump(self.problems, f, indent=4, separators=(",", ": "))

    def download(self, index: int, link: WebElement) -> None:
        number = f"{index:02}"

        if (href := link.get_attribute("href")) is None:
            print(f"Failed to download the test case: {number}")
            sys.exit(1)

        contest_id = href.split("/")[-3]
        problem_id = href.split("/")[-1]
        problem_dir = Path(self.contest_title, number, "test")
        problem_url = f"https://atcoder.jp/contests/{contest_id}/tasks/{problem_id}"
        command = ["oj", "d", "-d", str(problem_dir), problem_url]
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            check=True,
        )
        print(f"Downloaded the test case: {number} {problem_id}")

        problem: New.Problem = {
            "contest_id": contest_id,
            "problem_id": problem_id,
            "url": problem_url,
        }
        self.problems[index] = problem

    def run(self) -> None:
        for index, link in enumerate(self.links, start=1):
            self.download(index, link)

        self.create_info()


class Submit:
    def __init__(self, file: str) -> None:
        info_path = Path(f"../{INFO_FILE}")
        file_path = Path(file)

        if not info_path.exists():
            Submit.print_no_file_error(info_path)

        if not file_path.exists():
            Submit.print_no_file_error(file_path)

        self.info_path = info_path
        self.file = file

    @staticmethod
    def print_no_file_error(path: Path) -> None:
        print(f"Error: '{path}' does not exist.")
        sys.exit(1)

    def run(self) -> None:
        with self.info_path.open() as f:
            info = json.load(f)

        problem_num = int(Path.cwd().name)
        url = info[str(problem_num)]["url"]

        command = ["oj", "s", url, self.file]
        subprocess.run(
            command,
            check=True,
        )


def new(args: Args) -> None:
    New(args.url).run()


def submit(args: Args) -> None:
    Submit(args.file).run()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("AtCoder Problems command line tools")
    subparsers = parser.add_subparsers(required=True)

    new_message = "create a new contest project directory"
    new_cmd = subparsers.add_parser("new", help=new_message, aliases=["n"])
    new_cmd.add_argument("url", help="the URL of the contest")
    new_cmd.set_defaults(func=new)

    submit_message = "submit the solution"
    submit_cmd = subparsers.add_parser("submit", help=submit_message, aliases=["s"])
    submit_cmd.add_argument("file", help="the file to submit")
    submit_cmd.set_defaults(func=submit)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
