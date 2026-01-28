"""
2. Meeting Room Scheduler
-------------------------

Implement a meeting room scheduler with conflict detection.

You are given a list of queries. Each query is a list of strings.

Write:
    solution(queries: list[list[str]]) -> list[str]

All times are integer minutes. Intervals are half-open: [start, end).
Two events do NOT overlap if one ends exactly when the other starts.

Queries
~~~~~~~

1) ["BOOK", room, start, end, title]
   - Books a new event in `room` if:
       * start < end
       * it does not overlap any existing event in the same room
   - Output: "true" if booked, else "false".

2) ["CANCEL", room, title]
   - Cancels exactly one event with the given title in the room.
   - If multiple events have the same title, cancel the one with the earliest start time.
   - Output: "true" if an event was canceled, else "false".

3) ["MOVE", room, title, new_start, new_end]
   - Finds the event with `title` in the room (earliest start if multiple).
   - Attempts to move it to [new_start, new_end).
   - The move succeeds only if:
       * new_start < new_end
       * the moved event would not overlap any other event in the room
         (excluding itself)
   - Output: "true" on success, else "false".

4) ["FREE", room, start, end]
   - Returns the total number of free minutes within [start, end) in the room,
     subtracting any overlaps with existing events.
   - If start >= end, output "0".

5) ["AGENDA", room]
   - Returns all events in the room sorted by (start, end, title).
   - Output format:
       "start-end:title,start-end:title,..."
     If there are no events, output "".

Return value
~~~~~~~~~~~~

Return a list of outputs (strings) for each query that produces output:
BOOK, CANCEL, MOVE, FREE, AGENDA (in that order of occurrence).
"""

from __future__ import annotations


def solution(queries: list[list[str]]) -> list[str]:
    agenda: dict[str, list[tuple[int, int, str]]] = {}
    outputs: list[str] = []

    for query in queries:
        queryType = query[0]
        
        if queryType == "BOOK":
            outputs.append(bookHandler(query, agenda))
        elif queryType == "CANCEL":
            outputs.append(cancelHandler(query, agenda))
        elif queryType == "MOVE":
            outputs.append(moveHandler(query, agenda))
        elif queryType == "FREE":
            outputs.append(freeHandler(query, agenda))
        elif queryType == "AGENDA":
            outputs.append(agendaHandler(query, agenda))
        else:
            raise ValueError(f"Unknown query type: {queryType!r}")

    return outputs


def bookHandler(query, agenda):
    room = str(query[1])
    start = int(query[2])
    end = int(query[3])
    title = str(query[4])

    if start >= end:
        return "false"

    # Get room dict values
    events = agenda.setdefault(room, [])

    # If start is before previous ends, and end is after previous starts, return old agenda
    for agenda_start, agenda_end, agenda_title in events:
        if start < agenda_end and agenda_start < end:
            return "false"

    # We know now that the event can be booked
    events.append((start, end, title))
    events.sort(key=lambda x: (x[0], x[1], x[2]))
    return "true"
    

def cancelHandler(query, agenda):
    room = str(query[1])
    title = str(query[2])

    events = agenda.get(room, [])
    idx = None
    best = None
    for i, (agenda_start, agenda_end, agenda_title) in enumerate(events):
        if agenda_title != title:
            continue
        cand = (agenda_start, agenda_end, agenda_title)
        if best is None or cand < best:
            best = cand
            idx = i
    if idx is None:
        return "false"
    del events[idx]
    return "true"

            

def moveHandler(query, agenda):
    room = str(query[1])
    title = str(query[2])
    new_start = int(query[3])
    new_end = int(query[4])

    if new_start >= new_end:
        return "false"

    events = agenda.get(room, [])
    idx = None
    best = None
    for i, (agenda_start, agenda_end, agenda_title) in enumerate(events):
        if agenda_title != title:
            continue
        cand = (agenda_start, agenda_end, agenda_title)
        if best is None or cand < best:
            best = cand
            idx = i
    if idx is None:
        return "false"

    old_event = events.pop(idx)

    # Fail check if we cannot add event to cleared agenda
    for agenda_start, agenda_end, agenda_title in events:
        if new_start < agenda_end and agenda_start < new_end:
            # Fail move and re-add the event
            events.append(old_event)
            events.sort(key=lambda x: (x[0], x[1], x[2]))
            return "false"

    # All checks passed, move event (just re-add it)
    events.append((new_start, new_end, title))
    events.sort(key=lambda x: (x[0], x[1], x[2]))
    return "true"


def freeHandler(query, agenda):
    room = str(query[1])
    start = int(query[2])
    end = int(query[3])

    if start >= end:
        return "0"

    events = agenda.get(room, [])
    segments: list[tuple[int, int]] = []
    for agenda_start, agenda_end, agenda_title in events:
        ss, ee = max(start, agenda_start), min(end, agenda_end)
        if ss < ee:
            segments.append((ss, ee))

    segments.sort()
    covered = 0
    cur_s = None
    cur_e = None
    for ss, ee in segments:
        if cur_s is None:
            cur_s, cur_e = ss, ee
            continue
        if ss <= cur_e:
            cur_e = max(cur_e, ee)
        else:
            covered += cur_e - cur_s
            cur_s, cur_e = ss, ee
    if cur_s is not None and cur_e is not None:
        covered += cur_e - cur_s

    return str((end - start) - covered)
            
def agendaHandler(query, agenda):
    room = str(query[1])
    events = agenda.get(room, [])
    if not events:
        return ""
    
    # Format output
    events_sorted = sorted(events, key=lambda x: (x[0], x[1], x[2]))
    return ",".join(f"{agenda_start}-{agenda_end}:{agenda_title}" for agenda_start, agenda_end, agenda_title in events_sorted)
    


if __name__ == "__main__":
    sample = [
        ["BOOK", "R1", "10", "20", "standup"],
        ["BOOK", "R1", "20", "30", "retro"],
        ["BOOK", "R1", "15", "25", "overlap"],
        ["AGENDA", "R1"],
        ["FREE", "R1", "0", "40"],
    ]
    try:
        print(solution(sample))
    except NotImplementedError:
        import sys

        print(
            "Implement solution() in this file, then run: python3 Verification/verify_02_meeting_room_scheduler.py",
            file=sys.stderr,
        )
