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
    peopleTracker = {}
    WATracker = {}
    timeTracker = {}

    for query in queries:
        if query[0] == "SUBMIT":
            peopleTracker, WATracker, timeTracker = submitHandler(query, peopleTracker, WATracker, timeTracker)

        if query[0] == "SCOREBOARD":
            scoreboard = scoreboardHandler(query, peopleTracker, WATracker, timeTracker)

    return scoreboard


        
def submitHandler(query: list[str], peopleTracker: dict[str, list[str]], WATracker: dict[str, int], timeTracker: dict[str, int]) -> list[str]:
    time = int(query[1])
    user = str(query[2])
    problem = str(query[3])
    verdict = str(query[4])

    if user not in peopleTracker:
        peopleTracker[user] = [problem]
    if user not in WATracker:
        WATracker[user] = 0
    if user not in timeTracker:
        timeTracker[user] = time

    if verdict == "WA":
        WATracker[user] += 1    
    if verdict == "AC":
        peopleTracker[user].append(problem)
        timeTracker[user] = time

    return peopleTracker, WATracker, timeTracker


def scoreboardHandler(query: list[str], scoreboard: list[str], peopleTracker: dict[str, list[str]], WATracker: dict[str, int], timeTracker: dict[str, int]) -> list[str]:
    k = int(query[2])
    scoreboardStruct = []
    for user in peopleTracker:
        problemsSolved = len(peopleTracker[user])
        penalty = timeTracker[user] + 20 * WATracker[user]
        scoreboardStruct.append([user, problemsSolved, penalty])

    constructScoreboard(scoreboardStruct, k)
 

def constructScoreboard(scoreboardStruct: list[list[str,int,int]], k:int) -> str:
    scoreboard = ""



    


    

    




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
