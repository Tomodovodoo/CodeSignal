"""
1. Contest Scoreboard
--------------------

Implement a simplified contest scoreboard.

You are given a list of queries. Each query is a list of strings.

Write:
    solution(queries: list[list[str]]) -> list[str]

Queries
~~~~~~~

1) ["SUBMIT", t, user, problem, verdict]
   - t: integer timestamp (string). Queries are in non-decreasing t.
   - verdict is "AC" or "WA".
   - For each (user, problem):
       * Before the first "AC": "WA" increases wrong-attempts by 1.
       * The first "AC" marks the problem as solved at time t.
       * After a problem is solved, later submissions for that problem are ignored.
   - Per solved problem, add penalty:
       penalty = time_of_first_AC + 20 * (wrong_attempts_before_first_AC)

2) ["SCOREBOARD", t, k]
   - Return a single string describing the top k users who have solved >= 1 problem.
   - Ranking:
       1) More solved problems first
       2) Lower total penalty next
       3) Lexicographically smaller username next
   - Output format:
       "user:solved:penalty,user:solved:penalty,..."
     If there are no users with solved >= 1, output "" (empty string).

Return value
~~~~~~~~~~~~

Return a list of outputs (strings) for each SCOREBOARD query, in order.

Notes
~~~~~
 - Use only the Python standard library.
 - Keep it correct over clever. Hidden tests will probe edge cases.
"""

from __future__ import annotations


def solution(queries: list[list[str]]) -> list[str]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    # Simple smoke example (not exhaustive).
    sample = [
        ["SUBMIT", "10", "alice", "A", "WA"],
        ["SUBMIT", "15", "alice", "A", "AC"],  # penalty = 15 + 20*1 = 35
        ["SUBMIT", "20", "bob", "A", "AC"],  # penalty = 20
        ["SCOREBOARD", "21", "5"],  # bob:1:20,alice:1:35
    ]
    try:
        print(solution(sample))
    except NotImplementedError:
        import sys

        print("Implement solution() in this file, then run: python3 Verification/verify_01_contest_scoreboard.py", file=sys.stderr)
