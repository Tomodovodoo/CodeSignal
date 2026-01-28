from __future__ import annotations

import random
from copy import deepcopy

from _harness import assert_equal, assert_is_list_of_str, load_solution, run_solution


def _overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return a_start < b_end and b_start < a_end


def _oracle(queries: list[list[str]]) -> list[str]:
    rooms: dict[str, list[tuple[int, int, str]]] = {}  # room -> [(start,end,title)]
    outputs: list[str] = []

    for q in queries:
        kind = q[0]
        if kind == "BOOK":
            room, start_s, end_s, title = q[1], q[2], q[3], q[4]
            start, end = int(start_s), int(end_s)
            if start >= end:
                outputs.append("false")
                continue

            events = rooms.setdefault(room, [])
            if any(_overlaps(start, end, s, e) for s, e, _ in events):
                outputs.append("false")
                continue

            events.append((start, end, title))
            events.sort(key=lambda x: (x[0], x[1], x[2]))
            outputs.append("true")

        elif kind == "CANCEL":
            room, title = q[1], q[2]
            events = rooms.get(room, [])
            idx = None
            best: tuple[int, int, str] | None = None
            for i, ev in enumerate(events):
                if ev[2] != title:
                    continue
                if best is None or (ev[0], ev[1], ev[2]) < (best[0], best[1], best[2]):
                    best = ev
                    idx = i
            if idx is None:
                outputs.append("false")
            else:
                del events[idx]
                outputs.append("true")

        elif kind == "MOVE":
            room, title = q[1], q[2]
            new_start, new_end = int(q[3]), int(q[4])
            if new_start >= new_end:
                outputs.append("false")
                continue

            events = rooms.get(room, [])
            idx = None
            best: tuple[int, int, str] | None = None
            for i, ev in enumerate(events):
                if ev[2] != title:
                    continue
                if best is None or (ev[0], ev[1], ev[2]) < (best[0], best[1], best[2]):
                    best = ev
                    idx = i
            if idx is None or best is None:
                outputs.append("false")
                continue

            old = events.pop(idx)
            if any(_overlaps(new_start, new_end, s, e) for s, e, _ in events):
                events.append(old)
                events.sort(key=lambda x: (x[0], x[1], x[2]))
                outputs.append("false")
                continue

            events.append((new_start, new_end, title))
            events.sort(key=lambda x: (x[0], x[1], x[2]))
            outputs.append("true")

        elif kind == "FREE":
            room, start_s, end_s = q[1], q[2], q[3]
            start, end = int(start_s), int(end_s)
            if start >= end:
                outputs.append("0")
                continue

            events = rooms.get(room, [])
            segments: list[tuple[int, int]] = []
            for s, e, _ in events:
                ss, ee = max(start, s), min(end, e)
                if ss < ee:
                    segments.append((ss, ee))
            segments.sort()

            covered = 0
            cur_s, cur_e = None, None
            for ss, ee in segments:
                if cur_s is None:
                    cur_s, cur_e = ss, ee
                    continue
                if ss <= cur_e:  # merge touching/overlapping
                    cur_e = max(cur_e, ee)
                else:
                    covered += cur_e - cur_s
                    cur_s, cur_e = ss, ee
            if cur_s is not None and cur_e is not None:
                covered += cur_e - cur_s

            outputs.append(str((end - start) - covered))

        elif kind == "AGENDA":
            room = q[1]
            events = rooms.get(room, [])
            if not events:
                outputs.append("")
            else:
                events_sorted = sorted(events, key=lambda x: (x[0], x[1], x[2]))
                outputs.append(",".join(f"{s}-{e}:{t}" for s, e, t in events_sorted))

        else:
            raise ValueError(f"Unknown query type: {kind!r}")

    return outputs


def _random_case(rng: random.Random) -> list[list[str]]:
    rooms = ["R1", "R2", "R3"]
    titles = ["standup", "retro", "1:1", "planning", "demo"]
    queries: list[list[str]] = []
    for _ in range(rng.randint(40, 120)):
        op = rng.choices(
            population=["BOOK", "CANCEL", "MOVE", "FREE", "AGENDA"],
            weights=[0.45, 0.12, 0.18, 0.18, 0.07],
        )[0]
        room = rng.choice(rooms)
        if op == "BOOK":
            start = rng.randint(0, 120)
            end = start + rng.randint(0, 40)  # may be invalid (0)
            title = rng.choice(titles)
            queries.append(["BOOK", room, str(start), str(end), title])
        elif op == "CANCEL":
            title = rng.choice(titles)
            queries.append(["CANCEL", room, title])
        elif op == "MOVE":
            title = rng.choice(titles)
            start = rng.randint(0, 120)
            end = start + rng.randint(0, 40)
            queries.append(["MOVE", room, title, str(start), str(end)])
        elif op == "FREE":
            start = rng.randint(0, 120)
            end = rng.randint(0, 160)
            queries.append(["FREE", room, str(start), str(end)])
        else:
            queries.append(["AGENDA", room])
    return queries


def main() -> None:
    candidate = load_solution("02_meeting_room_scheduler.py")

    cases: list[list[list[str]]] = [
        [
            ["BOOK", "R1", "10", "20", "standup"],
            ["BOOK", "R1", "20", "30", "retro"],
            ["BOOK", "R1", "15", "25", "overlap"],
            ["AGENDA", "R1"],
            ["FREE", "R1", "0", "40"],
        ],
        [
            ["BOOK", "R1", "10", "10", "bad"],
            ["FREE", "R1", "5", "5"],
            ["AGENDA", "R1"],
        ],
        [
            ["BOOK", "R1", "0", "10", "a"],
            ["BOOK", "R1", "10", "20", "a"],
            ["CANCEL", "R1", "a"],
            ["AGENDA", "R1"],
            ["MOVE", "R1", "a", "5", "15"],  # should fail (overlaps none? depends which 'a' remains)
            ["AGENDA", "R1"],
        ],
    ]

    rng = random.Random(2026)
    for _ in range(30):
        cases.append(_random_case(rng))

    try:
        for i, queries in enumerate(cases, start=1):
            expected = _oracle(deepcopy(queries))
            got = run_solution(candidate, deepcopy(queries), context=f"case {i}")
            assert_is_list_of_str(got, context=f"case {i}: return type")
            assert_equal(got, expected, context=f"case {i}")
    except AssertionError as e:
        print(f"verify_02_meeting_room_scheduler: FAIL\n{e}")
        raise SystemExit(1)

    print("verify_02_meeting_room_scheduler: PASS")


if __name__ == "__main__":
    main()
