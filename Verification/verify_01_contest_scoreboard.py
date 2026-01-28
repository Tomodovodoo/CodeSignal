from __future__ import annotations

import random
from copy import deepcopy

from _harness import assert_equal, assert_is_list_of_str, load_solution, run_solution


def _oracle(queries: list[list[str]]) -> list[str]:
    # user -> problem -> (wrong_before_ac, solved, ac_time)
    per_user_problem: dict[str, dict[str, list[int | bool]]] = {}
    totals: dict[str, tuple[int, int]] = {}  # user -> (solved, penalty)
    outputs: list[str] = []

    for q in queries:
        kind = q[0]
        if kind == "SUBMIT":
            t = int(q[1])
            user = q[2]
            problem = q[3]
            verdict = q[4]

            user_state = per_user_problem.setdefault(user, {})
            problem_state = user_state.get(problem)
            if problem_state is None:
                # [wrong, solved(bool), ac_time]
                problem_state = [0, False, -1]
                user_state[problem] = problem_state

            wrong = int(problem_state[0])
            solved = bool(problem_state[1])

            if solved:
                continue

            if verdict == "WA":
                problem_state[0] = wrong + 1
            elif verdict == "AC":
                problem_state[1] = True
                problem_state[2] = t
                solved_count, penalty_sum = totals.get(user, (0, 0))
                totals[user] = (solved_count + 1, penalty_sum + t + 20 * wrong)
            else:
                raise ValueError(f"Unknown verdict: {verdict!r}")

        elif kind == "SCOREBOARD":
            k = int(q[2])
            ranked = [
                (user, solved, penalty)
                for user, (solved, penalty) in totals.items()
                if solved > 0
            ]
            ranked.sort(key=lambda x: (-x[1], x[2], x[0]))
            top = ranked[:k]
            if not top:
                outputs.append("")
            else:
                outputs.append(",".join(f"{u}:{s}:{p}" for u, s, p in top))
        else:
            raise ValueError(f"Unknown query type: {kind!r}")

    return outputs


def _generate_random_case(rng: random.Random, *, users: list[str], problems: list[str]) -> list[list[str]]:
    t = 0
    queries: list[list[str]] = []
    # Ensure at least one SCOREBOARD.
    n = rng.randint(40, 120)
    for _ in range(n):
        t += rng.randint(0, 3)
        if rng.random() < 0.2:
            k = rng.randint(1, 6)
            queries.append(["SCOREBOARD", str(t), str(k)])
            continue

        user = rng.choice(users)
        problem = rng.choice(problems)
        verdict = "AC" if rng.random() < 0.35 else "WA"
        queries.append(["SUBMIT", str(t), user, problem, verdict])

    if queries[-1][0] != "SCOREBOARD":
        t += 1
        queries.append(["SCOREBOARD", str(t), "10"])
    return queries


def main() -> None:
    candidate = load_solution("01_contest_scoreboard.py")

    cases: list[list[list[str]]] = [
        [
            ["SUBMIT", "10", "alice", "A", "WA"],
            ["SUBMIT", "15", "alice", "A", "AC"],  # 35
            ["SUBMIT", "20", "bob", "A", "AC"],  # 20
            ["SCOREBOARD", "21", "5"],
        ],
        [
            ["SUBMIT", "1", "alice", "A", "AC"],
            ["SUBMIT", "1", "bob", "A", "AC"],
            ["SUBMIT", "2", "alice", "B", "WA"],
            ["SUBMIT", "3", "alice", "B", "AC"],
            ["SUBMIT", "4", "bob", "B", "WA"],
            ["SUBMIT", "6", "bob", "B", "AC"],
            ["SCOREBOARD", "7", "10"],
        ],
        [
            ["SUBMIT", "1", "u", "P", "WA"],
            ["SUBMIT", "2", "u", "P", "WA"],
            ["SUBMIT", "3", "u", "P", "WA"],
            ["SCOREBOARD", "4", "3"],  # no solved users yet
            ["SUBMIT", "5", "u", "P", "AC"],  # penalty=5+60=65
            ["SCOREBOARD", "5", "3"],
            ["SUBMIT", "6", "u", "P", "WA"],  # ignored post-AC
            ["SCOREBOARD", "7", "3"],
        ],
    ]

    rng = random.Random(1337)
    for _ in range(25):
        cases.append(
            _generate_random_case(
                rng, users=["alice", "bob", "carl", "dana", "erin"], problems=["A", "B", "C", "D"]
            )
        )

    try:
        for i, queries in enumerate(cases, start=1):
            expected = _oracle(deepcopy(queries))
            got = run_solution(candidate, deepcopy(queries), context=f"case {i}")
            assert_is_list_of_str(got, context=f"case {i}: return type")
            assert_equal(got, expected, context=f"case {i}")
    except AssertionError as e:
        print(f"verify_01_contest_scoreboard: FAIL\n{e}")
        raise SystemExit(1)

    print("verify_01_contest_scoreboard: PASS")


if __name__ == "__main__":
    main()
