from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Callable, TypeVar

T = TypeVar("T")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_module_from_path(path: Path) -> ModuleType:
    path = path.resolve()
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to import module from path: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_solution(test_filename: str) -> Callable[[list[list[str]]], list[str]]:
    tests_dir = repo_root() / "Tests"
    path = tests_dir / test_filename
    if not path.exists():
        raise FileNotFoundError(f"Missing test file: {path}")

    module = load_module_from_path(path)
    sol = getattr(module, "solution", None)
    if not callable(sol):
        raise TypeError(f"{path} must define a callable solution(queries) function")
    return sol


def assert_is_list_of_str(value: object, *, context: str) -> None:
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        raise AssertionError(f"{context}: expected list[str], got {type(value).__name__}: {value!r}")


def assert_equal(got: T, expected: T, *, context: str) -> None:
    if got != expected:
        raise AssertionError(f"{context}:\n  expected={expected!r}\n       got={got!r}")


def run_solution(
    solution: Callable[[list[list[str]]], list[str]],
    queries: list[list[str]],
    *,
    context: str,
) -> list[str]:
    try:
        return solution(queries)
    except NotImplementedError as e:
        raise AssertionError(f"{context}: solution() is not implemented") from e
    except Exception as e:  # pragma: no cover
        raise AssertionError(f"{context}: solution() raised {type(e).__name__}: {e}") from e
