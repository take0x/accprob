import argparse
from pathlib import Path
from typing import Callable
from urllib.parse import ParseResult, urlparse

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
    file: Path | None
    base_dir: Path
    func: Callable

    @staticmethod
    def from_argparse(args: argparse.Namespace) -> "TypedArgs":
        print(args)
        args.url = set_default(args, "url", str)
        args.file = set_default(args, "file", Path)
        args.base_dir = set_default(args, "base_dir", Path, Path.cwd())
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
