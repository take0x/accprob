import argparse
import json
from pathlib import Path

import requests
from onlinejudge import dispatch
from onlinejudge.service.atcoder import AtCoderProblem

from .models import AtCoderProblemAPIResponse, HttpStatus, TypedArgs


class AtCoderProblems:
    def __init__(self, url: str) -> None:
        """
        Initialize the AtCoderProblems class.

        Args:
            url (str | ParseResult): The URL of AtCoder Problems.
            (ex: https://kenkoooo.com/atcoder/#/contest/show/<UUID>)
        """
        self.url = url
        self.api_url = self.url.replace(
            "atcoder/#/contest/show", "atcoder/internal-api/contest/get"
        )
        self.cache_dir = Path.cwd() / ".accprob"
        self.cache_dir.mkdir(exist_ok=True, parents=True)
        self.create_cache()

    @staticmethod
    def create_problem_url_from_problem_id(problem_id: str) -> str:
        return f"https://atcoder.jp/contests/{problem_id[:-2].replace('_', '-')}/tasks/{problem_id}"

    @staticmethod
    def from_url(url: str) -> "AtCoderProblems":
        """
        Create AtCoderProblems instance from URL. (いる？)
        """  # noqa: RUF002
        return AtCoderProblems(url)

    def create_cache(self) -> None:
        """
        Cache the test cases of the contest.
        """
        with (self.cache_dir / "current.json").open("w") as f:
            json.dump({"url": self.url, "api_url": self.api_url}, f)

        # if (self.cache_dir / "problems.json").exists() and (self.cache_dir / "problems.json").stat()
        # with (self.cache_dir / "problems.json").open() as f:
        #     url = "https://kenkoooo.com/atcoder/resources/problems.json"
        #     res = requests.get(url, timeout=10)
        #     if res.status_code == HttpStatus.OK:
        #         json.dump(res.json(), f)
        #     else:
        #         raise Exception("Error: Failed to get the problems data.")

    def download(self, base_dir: str | Path | None) -> None:
        """
        Download the test cases of the contest.
        """
        if base_dir is None:
            base_dir = Path.cwd()

        base_dir = Path(base_dir)

        res = requests.get(self.api_url, timeout=10)

        if res.status_code == HttpStatus.OK:
            data: AtCoderProblemAPIResponse = AtCoderProblemAPIResponse(**res.json())
        else:
            raise Exception("Error: Failed to get the contest data.")

        contest_dir = base_dir / data.info.title
        contest_dir.mkdir(parents=True, exist_ok=True)

        with (contest_dir / "info.json").open("w") as f:
            json.dump(
                data.model_dump(),
                f,
                ensure_ascii=False,
            )

        for problem in data.problems:
            problem_dir = contest_dir / f"{problem.order:02}-{problem.id}"
            problem_dir.mkdir(parents=True, exist_ok=True)
            problem_data = dispatch.problem_from_url(
                self.create_problem_url_from_problem_id(problem.id)
            )
            try:
                if problem_data is None:
                    raise Exception(
                        "Error: Failed to get the problem data.", problem.id
                    )
                problem_data.download_sample_cases()
            except Exception as e:
                print(e)
                continue

            print(problem.order, problem_data)

    def test(self, file: Path) -> None:
        """
        Test the solution.
        """

    def submit(self, file: Path) -> None:
        """
        Submit the solution to the contest.

        Args:
            file (Path): The file to submit.
        """


def parse_args() -> TypedArgs:
    parser = argparse.ArgumentParser("AtCoder Problems command line tools")
    subparsers = parser.add_subparsers(required=True)
    d = subparsers.add_parser(
        "download",
        description="Download the test cases of the contest",
        help="Require the URL of the contest",
        aliases=["d"],
    )
    d.add_argument("url", metavar="<AtCoder Problem URL>", help="URL of the contest")
    d.add_argument(
        "--dir",
        metavar="<Directory Path>",
        help=f"The directory to create contest directory. \
            default: currnet directory ({Path.cwd()})",
        default=Path.cwd(),
    )

    def download_hook(args: TypedArgs) -> None:
        AtCoderProblems(args.url).download(args.base_dir)

    d.set_defaults(func=download_hook)

    s = subparsers.add_parser(
        "submit",
        description="Submit the solution to the contest",
        help="Require the file to submit",
        aliases=["s"],
    )
    s.add_argument("file", metavar="<File Path>", help="The file to submit")

    def submit_hook(args: TypedArgs) -> None:
        if args.file is not None:
            AtCoderProblems(args.url).submit(args.file)
        else:
            print("Error: 'File' is required.")
            parser.print_help()

    s.set_defaults(func=submit_hook)

    return TypedArgs.from_argparse(parser.parse_args())


def main() -> None:
    args: TypedArgs = parse_args()
    args.func(args)


if __name__ == "__main__":
    # https://kenkoooo.com/atcoder/#/contest/show/e4b1a4f8-2043-4d70-8437-663152a8b700
    main()
