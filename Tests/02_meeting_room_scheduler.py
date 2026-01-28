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
    # Agenda, Dictionary of start time key: list of (start time, end time, title)
    agenda = dict[int, list[tuple[int, int, str]]]

    for query in queries:
        queryType = query[0]
        
        if queryType == "BOOK":
            agenda = bookHandler(query, agenda)
        elif queryType == "CANCEL":
            agenda = cancelHandler(query, agenda)
        elif queryType == "MOVE":
            agenda = moveHandler(query, agenda)
        elif queryType == "FREE":
            agenda = freeHandler(query, agenda)
        elif queryType == "AGENDA":
            print(agendaHandler(query, agenda))


    
def bookHandler(query, agenda):
    room = str(query[1])
    start = int(query[2])
    end = int(query[3])
    title = str(query[4])

def cancelHandler():

def moveHandler():

def freeHandler():

def agendaHandler():


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
