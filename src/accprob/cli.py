import argparse
import json
from datetime import datetime, timedelta, timezone
from logging import basicConfig, getLogger
from pathlib import Path
from time import sleep

import requests
from onlinejudge import dispatch

from .models import (
    AtCoderProblem,
    AtCoderProblemAPIResponse,
    AtCoderProblemsMetadata,
    HttpStatus,
    TypedArgs,
)
from .runner import JudgeRunner

JST = timezone(timedelta(hours=+9), "JST")

basicConfig(level="INFO")
getLogger("onlinejudge._implementation.utils").setLevel("ERROR")
logger = getLogger(__name__)


class AtCoderProblems:
    def __init__(self, url: str, base_dir: str | Path | None = None) -> None:
        """
        Initialize the AtCoderProblems class.

        Args:
            url (str | ParseResult): The URL of AtCoder Problems.
            (ex: https://kenkoooo.com/atcoder/#/contest/show/<Contest ID>)
        """

        if base_dir is None:
            base_dir = Path.cwd()
        base_dir = Path(base_dir) if isinstance(base_dir, str) else base_dir

        if url:  # URLが指定されている場合
            logger.info("Fetching the contest data from %s", url)
            self.url = url
            self.api_url = self.url.replace(
                "atcoder/#/contest/show", "atcoder/internal-api/contest/get"
            )  # APIのURLに変換
            if (
                res := requests.get(self.api_url, timeout=10)
            ).status_code == HttpStatus.OK:
                res = res.json()
                res["problems"] = [AtCoderProblem(**x) for x in res["problems"]]
                self.data: AtCoderProblemAPIResponse = AtCoderProblemAPIResponse(**res)
            else:
                logger.error("Error: Failed to get the contest data.")
                return

            self.contest_dir = base_dir / self.data.info.title
            self.write_cache(base_dir / ".accprob")  # キャッシュを作成
            self.contest_dir.mkdir(parents=True, exist_ok=True)

            with (self.contest_dir / "info.json").open("w") as f:
                json.dump(
                    {
                        "url": self.url,
                        "api_url": self.api_url,
                        "data": self.data.model_dump(),
                    },
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
        elif (
            base_dir / "info.json"
        ).exists():  # カレントディレクトリ直下にinfo.jsonが存在する場合
            logger.info("mode: base_dir / 'info.json'")
            logger.info("Fetching the contest data from %s", base_dir)
            with (base_dir / "info.json").open("r") as f:
                meta = json.load(f)
                self.url = meta["url"]
                data = meta["data"]
            self.data = AtCoderProblemAPIResponse(**data)
            self.contest_dir = base_dir.parent / self.data.info.title

        elif (base_dir / ".accprob" / "current.json").exists():
            logger.info("mode: base_dir / '.accprob' / 'current.json'")
            logger.info("Fetching the contest data from %s", base_dir)
            # カレントディレクトリ直下にinfo.jsonが存在しないが、
            # 直下の.accprobディレクトリ内にcurrent.jsonが存在する場合
            # （キャッシュがある場合）  # noqa: RUF003
            with (base_dir / ".accprob" / "current.json").open("r") as f:
                meta = json.load(f)
                self.url = meta["url"]
                self.contest_dir = base_dir / meta["title"]

            if not self.contest_dir.exists():
                msg = (
                    f"Failed to get the contest data from '{self.contest_dir}'. "
                    "Please run 'accprob download' first."
                )
                raise FileNotFoundError(msg)

            with (self.contest_dir / "info.json").open("r") as f:
                data = json.load(f)
                self.data = AtCoderProblemAPIResponse(**data["data"])
        else:
            logger.error("Error: Failed to get the contest data.")
            return
        self.contest_dir.mkdir(parents=True, exist_ok=True)

    def write_cache(self, cache_dir: Path) -> None:
        cache_dir.mkdir(parents=True, exist_ok=True)
        with (cache_dir / "current.json").open("w") as f:
            json.dump(
                {
                    "url": self.url,
                    "title": self.data.info.title,
                },
                f,
                ensure_ascii=False,
                indent=4,
            )

    @staticmethod
    def from_url(url: str) -> "AtCoderProblems":
        """
        Create AtCoderProblems instance from URL. (いる？)
        """  # noqa: RUF002
        return AtCoderProblems(url)

    def fetch_all_problems_metadata(self) -> list[AtCoderProblemsMetadata]:
        url = "https://kenkoooo.com/atcoder/resources/problems.json"
        if (res := requests.get(url, timeout=10)).status_code == HttpStatus.OK:
            return [AtCoderProblemsMetadata(**x) for x in res.json()]
        logger.error("Error: Failed to get the problems metadata.")
        return []

    def download(self) -> None:
        """
        Download the test cases of the contest.
        """
        all_problems_metadata = self.fetch_all_problems_metadata()

        for problem_index in self.data.problems:
            problem_dir = (
                self.contest_dir / f"{problem_index.order:02}-{problem_index.id}"
            )
            testcase_in_dir = problem_dir / "in"
            testcase_out_dir = problem_dir / "out"
            if (testcase_in_dir.exists() and testcase_out_dir.exists()) and (
                len(list(testcase_in_dir.iterdir())) > 0
                and len(list(testcase_out_dir.iterdir())) > 0
            ):
                logger.info(
                    "Skip: %s : %2d : %s",
                    self.data.info.title,
                    problem_index.order,
                    problem_index.id,
                )
                continue
            testcase_in_dir.mkdir(parents=True, exist_ok=True)
            testcase_out_dir.mkdir(parents=True, exist_ok=True)

            problem_metadata = next(
                filter(lambda x: x.id == problem_index.id, all_problems_metadata)
            )

            sleep(0.6)
            logger.info(
                "Downloading :%s:%2d:%s:from %s",
                self.data.info.title,
                problem_index.order,
                problem_index.id,
                problem_metadata.url,
            )
            problem = dispatch.problem_from_url(problem_metadata.url)
            if problem is None:
                logger.error("Error: Failed to get the problem data.")
                return
            testcases = problem.download_sample_cases()
            if not testcases:
                logger.info("Failed to get the test cases.")
            for testcase in testcases:
                with (
                    (testcase_in_dir / f"{testcase.name}.in").open("w") as in_f,
                    (testcase_out_dir / f"{testcase.name}.out").open("w") as out_f,
                ):
                    in_f.write(testcase.input_data.decode())
                    out_f.write(testcase.output_data.decode())

    def test(  # noqa: C901
        self,
        problem_key: str,
        bind_commands: list[str],
        *,
        not_confirm: bool = False,
        show_detail: bool = False,
    ) -> None:
        """
        Test the solution.
        """
        logger.info("contest dir=%s", self.contest_dir)
        logger.info("problem key=%s", problem_key)
        logger.info("not confirm=%s", not_confirm)
        logger.info("show detail=%s", show_detail)
        logger.info("bind commands=%s", bind_commands)
        target_problem = None

        if problem_key.isdigit():
            target_problem = self.data.problems[int(problem_key)]
        elif prob := tuple(filter(lambda x: problem_key in x.id, self.data.problems)):
            if not prob:
                msg = "Error: Problem not found."
                raise ValueError(msg)
            if len(prob) > 1:
                msg = (
                    "Ambiguous problem key. \n"
                    + "".join([f"{x.order:02}-{x.id}\n" for x in prob])
                    + "Error: Ambiguous problem key. Please specify more."
                )
                raise ValueError(msg)
            target_problem = next(
                filter(lambda x: problem_key in x.id, self.data.problems)
            )
        else:
            msg = "Problem not found."
            raise ValueError(msg)

        problem_dir = (
            self.contest_dir / f"{target_problem.order:02}-{target_problem.id}"
        )
        ans = "y"
        while not not_confirm:
            ans = input(f"Test {problem_dir}? ([Y]/n): ").lower()
            if ans in ["y", "n", ""]:
                break
        if ans == "n":
            return

        testcase_in_dir = problem_dir / "in"
        testcase_out_dir = problem_dir / "out"

        if not testcase_in_dir.exists() or not testcase_out_dir.exists():
            logger.error("Error: Test cases not found.")
            return

        runner = JudgeRunner(bind_commands, problem_dir)

        for testcase_in in sorted(testcase_in_dir.iterdir()):
            testcase_out = testcase_out_dir / testcase_in.with_suffix(".out").name
            if show_detail:
                result, meta = runner(
                    testcase_in,
                    testcase_out,
                    return_detail=True,
                )
                meta["input"] = testcase_in.read_text()
                meta["expected"] = testcase_out.read_text()
                print("\n" + "=" * 64, "\n")
                print(f"time: {meta['time']}[s]")
                print(f"return code: {meta['return_code']}\n")
                print(f"In:\n{meta['input']}")
                print(f"Your Out:\n{meta['answer']}")
                print(f"Expected:\n{meta['expected']}")

            else:
                print(
                    target_problem.id,
                    ":",
                    testcase_in.name,
                    "->",
                    testcase_out.name,
                    "->",
                    runner(testcase_in, testcase_out)[0],
                )

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
        "--directory",
        metavar="<Directory Path>",
        help=f"The directory to create contest directory. \
            default: currnet directory ({Path.cwd()})",
        default=Path.cwd(),
    )

    def download_hook(args: TypedArgs) -> None:
        AtCoderProblems(args.url, args.directory).download()

    t = subparsers.add_parser(
        "test",
        description="Test the solution",
        help="Require the file to test",
        aliases=["t"],
    )
    t.add_argument(
        "problem",
        metavar="<Problem Index> OR <Problem ID>",
        help="The problem index or ID to test. (ex: if the directory is '01-abc001_a', \
            the problem index is '01' and the problem ID is 'abc001_a')",
    )
    t.add_argument(
        "--skip-confirm",
        dest="skip_confirm",
        action="store_true",
        help="Skip the confirmation",
    )
    t.add_argument(
        "-y",
        "--yes",
        dest="skip_confirm",
        action="store_true",
        help="Skip the confirmation",
    )
    t.add_argument(
        "--show-detail",
        dest="show_detail",
        action="store_true",
        help="Show the detail of the test result",
    )
    t.add_argument(
        "--bind-commands",
        metavar="<Command>",
        help=(
            "Bind the command to test the solution. Tester will run"
            "`<Command> **/sample-*.in **/sample-*.out`)"
            "ex: python main.py"
            "**/<Problem_DIR>/sample-*.in **/<Problem_DIR>/sample-*.out"
        ),
        default="python main.py",
    )

    def test_hook(args: TypedArgs) -> None:
        AtCoderProblems(args.url, args.directory).test(
            args.problem,
            args.bind_commands,
            not_confirm=args.skip_confirm,
            show_detail=args.show_detail,
        )

    t.set_defaults(func=test_hook)

    d.set_defaults(func=download_hook)

    s = subparsers.add_parser(
        "submit",
        description="Submit the solution to the contest",
        help="Require the file to submit",
        aliases=["s"],
    )
    s.add_argument("file", metavar="<File Path>", help="The file to submit")

    def submit_hook(args: TypedArgs) -> None:
        AtCoderProblems(args.url).submit(args.file)

    s.set_defaults(func=submit_hook)
    return TypedArgs.from_argparse(parser.parse_args())


def main() -> None:
    args: TypedArgs = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
