from __future__ import annotations

import random
from copy import deepcopy
from typing import Any

from _harness import assert_equal, assert_is_list_of_str, load_solution, run_solution


def _oracle(queries: list[list[str]]) -> list[str]:
    # Use full-state snapshots for clarity; efficient solutions can do diffs.
    import copy

    states: list[dict[str, dict[str, str]]] = [{}]
    outputs: list[str] = []

    def cur() -> dict[str, dict[str, str]]:
        return states[-1]

    for q in queries:
        kind = q[0]
        if kind == "SET":
            key, field, value = q[1], q[2], q[3]
            cur().setdefault(key, {})[field] = value
        elif kind == "GET":
            key, field = q[1], q[2]
            outputs.append(cur().get(key, {}).get(field, ""))
        elif kind == "DELETE":
            key, field = q[1], q[2]
            if key in cur() and field in cur()[key]:
                del cur()[key][field]
                if not cur()[key]:
                    del cur()[key]
                outputs.append("true")
            else:
                outputs.append("false")
        elif kind == "FIELDS":
            key = q[1]
            fields = cur().get(key, {})
            if not fields:
                outputs.append("")
            else:
                items = sorted(fields.items(), key=lambda kv: kv[0])
                outputs.append(",".join(f"{f}={v}" for f, v in items))
        elif kind == "BEGIN":
            states.append(copy.deepcopy(cur()))
        elif kind == "COMMIT":
            if len(states) == 1:
                outputs.append("false")
            else:
                top = states.pop()
                states[-1] = top
                outputs.append("true")
        elif kind == "ROLLBACK":
            if len(states) == 1:
                outputs.append("false")
            else:
                states.pop()
                outputs.append("true")
        else:
            raise ValueError(f"Unknown query type: {kind!r}")

    return outputs


def _random_case(rng: random.Random) -> list[list[str]]:
    keys = ["k1", "k2", "k3"]
    fields = ["a", "b", "c", "d"]
    values = ["v1", "v2", "v3", "v4", "v5"]

    queries: list[list[str]] = []
    depth = 0
    for _ in range(rng.randint(60, 180)):
        op = rng.choices(
            population=["SET", "GET", "DELETE", "FIELDS", "BEGIN", "COMMIT", "ROLLBACK"],
            weights=[0.32, 0.18, 0.14, 0.10, 0.10, 0.08, 0.08],
        )[0]
        if op == "BEGIN":
            depth += 1
            queries.append(["BEGIN"])
            continue
        if op in ("COMMIT", "ROLLBACK"):
            # To keep sequences interesting, only sometimes call these at depth 0.
            if depth == 0 and rng.random() < 0.75:
                op = rng.choice(["SET", "GET", "DELETE", "FIELDS"])
            else:
                if op == "COMMIT" and depth > 0:
                    depth -= 1
                if op == "ROLLBACK" and depth > 0:
                    depth -= 1
                queries.append([op])
                continue

        key = rng.choice(keys)
        field = rng.choice(fields)
        if op == "SET":
            queries.append(["SET", key, field, rng.choice(values)])
        elif op == "GET":
            queries.append(["GET", key, field])
        elif op == "DELETE":
            queries.append(["DELETE", key, field])
        else:
            queries.append(["FIELDS", key])

    # Make sure we close out some transactions, but keep some at depth 0 too.
    for _ in range(rng.randint(0, 3)):
        queries.append([rng.choice(["COMMIT", "ROLLBACK"])])
    return queries


def main() -> None:
    candidate = load_solution("03_transactional_kv_store.py")

    cases: list[list[list[str]]] = [
        [
            ["SET", "u1", "name", "tom"],
            ["BEGIN"],
            ["SET", "u1", "name", "tom2"],
            ["GET", "u1", "name"],
            ["ROLLBACK"],
            ["GET", "u1", "name"],
        ],
        [
            ["BEGIN"],
            ["SET", "k", "a", "1"],
            ["BEGIN"],
            ["SET", "k", "a", "2"],
            ["COMMIT"],
            ["GET", "k", "a"],
            ["ROLLBACK"],
            ["GET", "k", "a"],
        ],
        [
            ["DELETE", "missing", "x"],
            ["COMMIT"],
            ["ROLLBACK"],
            ["SET", "k", "b", "v"],
            ["FIELDS", "k"],
            ["BEGIN"],
            ["DELETE", "k", "b"],
            ["FIELDS", "k"],
            ["ROLLBACK"],
            ["FIELDS", "k"],
        ],
    ]

    rng = random.Random(9001)
    for _ in range(35):
        cases.append(_random_case(rng))

    try:
        for i, queries in enumerate(cases, start=1):
            expected = _oracle(deepcopy(queries))
            got = run_solution(candidate, deepcopy(queries), context=f"case {i}")
            assert_is_list_of_str(got, context=f"case {i}: return type")
            assert_equal(got, expected, context=f"case {i}")
    except AssertionError as e:
        print(f"verify_03_transactional_kv_store: FAIL\n{e}")
        raise SystemExit(1)

    print("verify_03_transactional_kv_store: PASS")


if __name__ == "__main__":
    main()
