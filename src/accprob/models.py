import argparse
from collections.abc import Callable
from pathlib import Path

from pydantic import BaseModel


def set_default(
    target: object, attr: str, default_type: Callable, default_value: object = None
) -> object:
    if hasattr(target, attr):
        setattr(target, attr, default_type(getattr(target, attr)))
        return getattr(target, attr)
    setattr(target, attr, default_value)
    return default_value


class TypedArgs(BaseModel, argparse.Namespace):
    url: str
    problem: str
    directory: Path
    bind_commands: list[str]
    skip_confirm: bool
    show_detail: bool
    func: Callable

    @staticmethod
    def from_argparse(args: argparse.Namespace) -> "TypedArgs":
        args.url = set_default(args, "url", str, "")
        args.problem = set_default(args, "problem", str, "")
        args.directory = set_default(args, "directory", Path, Path.cwd())
        args.problem = set_default(args, "problem", str, "")
        args.skip_confirm = set_default(
            args, "skip_confirm", default_type=bool, default_value=False
        )
        args.show_detail = set_default(
            args, "show_detail", default_type=bool, default_value=False
        )
        args.bind_commands = set_default(
            args, "bind_commands", lambda x: x.split(" "), []
        )
        return TypedArgs(**vars(args))


class HttpStatus:
    OK = 200
    NOT_FOUND = 404
    BAD_REQUEST = 400


class AtCoderProblemInfo(BaseModel):
    id: str
    title: str
    memo: str
    owner_user_id: int
    start_epoch_second: int
    duration_second: int
    mode: str | None
    is_public: bool
    penalty_second: int


class AtCoderProblem(BaseModel):
    id: str
    point: None | int
    order: int


class AtCoderProblemAPIResponse(BaseModel):
    info: AtCoderProblemInfo
    problems: list[AtCoderProblem]


class AtCoderProblemsMetadata(BaseModel):
    id: str
    contest_id: str
    problem_index: str
    name: str
    title: str
    url: str = ""

    def __init__(
        self,
        **kwargs: dict[str, str],
    ) -> None:
        id_ = kwargs.get("id")
        contest_id = kwargs.get("contest_id")
        problem_index = kwargs.get("problem_index")
        name = kwargs.get("name")
        title = kwargs.get("title")

        super().__init__(
            id=id_,
            contest_id=contest_id,
            problem_index=problem_index,
            name=name,
            title=title,
            url=f"https://atcoder.jp/contests/{contest_id}/tasks/{id_}",
        )
