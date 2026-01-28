from __future__ import annotations

import random
from copy import deepcopy

from _harness import assert_equal, assert_is_list_of_str, load_solution, run_solution


def _alive(expiry: int | None, now: int) -> bool:
    return expiry is None or now < expiry


def _oracle(queries: list[list[str]]) -> list[str]:
    now = 0
    store: dict[str, dict[str, tuple[str, int | None]]] = {}
    backups: list[dict[str, dict[str, tuple[str, int | None]]]] = []
    outputs: list[str] = []

    for q in queries:
        kind = q[0]
        t = int(q[1])
        now = t

        if kind == "SET":
            key, field, value = q[2], q[3], q[4]
            store.setdefault(key, {})[field] = (value, None)

        elif kind == "SET_TTL":
            key, field, value, ttl_s = q[2], q[3], q[4], q[5]
            ttl = int(ttl_s)
            store.setdefault(key, {})[field] = (value, now + ttl)

        elif kind == "GET":
            key, field = q[2], q[3]
            val = store.get(key, {}).get(field)
            if val is None:
                outputs.append("")
            else:
                value, expiry = val
                outputs.append(value if _alive(expiry, now) else "")

        elif kind == "DELETE":
            key, field = q[2], q[3]
            val = store.get(key, {}).get(field)
            if val is None:
                outputs.append("false")
            else:
                _, expiry = val
                if not _alive(expiry, now):
                    outputs.append("false")
                else:
                    del store[key][field]
                    if not store[key]:
                        del store[key]
                    outputs.append("true")

        elif kind == "FIELDS":
            key = q[2]
            fields = store.get(key, {})
            alive_fields = [(f, v) for f, (v, exp) in fields.items() if _alive(exp, now)]
            if not alive_fields:
                outputs.append("")
            else:
                alive_fields.sort(key=lambda x: x[0])
                outputs.append(",".join(f"{f}={v}" for f, v in alive_fields))

        elif kind == "BACKUP":
            snapshot: dict[str, dict[str, tuple[str, int | None]]] = {}
            count = 0
            for key, fields in store.items():
                alive_items = {f: (v, exp) for f, (v, exp) in fields.items() if _alive(exp, now)}
                if alive_items:
                    snapshot[key] = dict(alive_items)
                    count += len(alive_items)
            backups.append(snapshot)
            outputs.append(str(count))

        elif kind == "RESTORE":
            idx = int(q[2])
            if not (0 <= idx < len(backups)):
                outputs.append("false")
            else:
                # Deep copy to prevent later mutations affecting stored snapshots.
                store = {k: dict(v) for k, v in backups[idx].items()}
                outputs.append("true")

        else:
            raise ValueError(f"Unknown query type: {kind!r}")

    return outputs


def _random_case(rng: random.Random) -> list[list[str]]:
    keys = ["k1", "k2", "k3"]
    fields = ["a", "b", "c", "d", "e"]
    values = ["x", "y", "z", "hello", "world"]

    now = 0
    backups = 0
    queries: list[list[str]] = []
    for _ in range(rng.randint(60, 160)):
        now += rng.randint(0, 3)
        op = rng.choices(
            population=["SET", "SET_TTL", "GET", "DELETE", "FIELDS", "BACKUP", "RESTORE"],
            weights=[0.18, 0.18, 0.20, 0.12, 0.12, 0.12, 0.08],
        )[0]
        if op == "BACKUP":
            backups += 1
            queries.append(["BACKUP", str(now)])
            continue
        if op == "RESTORE":
            # Sometimes pick an invalid restore index.
            if backups == 0 or rng.random() < 0.15:
                idx = backups + rng.randint(0, 3)
            else:
                idx = rng.randint(0, backups - 1)
            queries.append(["RESTORE", str(now), str(idx)])
            continue

        key = rng.choice(keys)
        field = rng.choice(fields)
        if op == "SET":
            queries.append(["SET", str(now), key, field, rng.choice(values)])
        elif op == "SET_TTL":
            ttl = rng.randint(0, 6)
            queries.append(["SET_TTL", str(now), key, field, rng.choice(values), str(ttl)])
        elif op == "GET":
            queries.append(["GET", str(now), key, field])
        elif op == "DELETE":
            queries.append(["DELETE", str(now), key, field])
        else:
            queries.append(["FIELDS", str(now), key])
    return queries


def main() -> None:
    candidate = load_solution("04_ttl_backup_store.py")

    cases: list[list[list[str]]] = [
        [
            ["SET_TTL", "10", "k", "a", "1", "5"],  # exp 15
            ["GET", "14", "k", "a"],  # 1
            ["GET", "15", "k", "a"],  # expired
            ["BACKUP", "16"],  # 0
        ],
        [
            ["SET", "1", "k", "a", "x"],
            ["SET_TTL", "2", "k", "b", "y", "2"],  # exp 4
            ["FIELDS", "3", "k"],  # a,b
            ["BACKUP", "3"],  # 2
            ["FIELDS", "4", "k"],  # only a
            ["RESTORE", "10", "0"],  # restore snapshot at t=3, but now=10 => b expired
            ["FIELDS", "10", "k"],  # only a
        ],
        [
            ["SET_TTL", "5", "k1", "a", "v", "0"],  # expires immediately
            ["GET", "5", "k1", "a"],
            ["DELETE", "5", "k1", "a"],
            ["BACKUP", "5"],
            ["RESTORE", "6", "0"],
            ["FIELDS", "6", "k1"],
        ],
    ]

    rng = random.Random(424242)
    for _ in range(40):
        cases.append(_random_case(rng))

    try:
        for i, queries in enumerate(cases, start=1):
            expected = _oracle(deepcopy(queries))
            got = run_solution(candidate, deepcopy(queries), context=f"case {i}")
            assert_is_list_of_str(got, context=f"case {i}: return type")
            assert_equal(got, expected, context=f"case {i}")
    except AssertionError as e:
        print(f"verify_04_ttl_backup_store: FAIL\n{e}")
        raise SystemExit(1)

    print("verify_04_ttl_backup_store: PASS")


if __name__ == "__main__":
    main()
