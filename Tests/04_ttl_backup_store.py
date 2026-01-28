"""
4. TTL + Backup/Restore Store (Hard)
-----------------------------------

Implement a time-aware key -> field -> value store with per-field TTL and backups.

You are given a list of queries. Each query is a list of strings.

Write:
    solution(queries: list[list[str]]) -> list[str]

Data model
~~~~~~~~~~

The store maps:
  key (string) -> field (string) -> value (string) with optional expiry time.

There is a global current time (integer seconds). For each query that includes `t`,
advance current time to int(t) BEFORE processing the query. Times are non-decreasing.

A field is expired if:
    current_time >= expiry_time
Expired fields behave as if they do not exist (GET returns "", etc.).

Queries
~~~~~~~

1) ["SET", t, key, field, value]
   - Sets key.field = value with NO expiry (overwrites any prior expiry).

2) ["SET_TTL", t, key, field, value, ttl]
   - Sets key.field = value with expiry_time = int(t) + int(ttl).
   - ttl may be 0 (meaning it expires immediately at time t).

3) ["GET", t, key, field]
   - Output: value, or "" if missing/expired.

4) ["DELETE", t, key, field]
   - Deletes the field if present and not expired at time t.
   - Output: "true" if deleted, else "false".

5) ["FIELDS", t, key]
   - Output a comma-separated list of "field=value" for non-expired fields of key.
   - Sort fields lexicographically by field name.
   - If none exist, output "".

6) ["BACKUP", t]
   - Creates a backup snapshot of the entire store at time t.
   - The snapshot should include only fields that are NOT expired at time t.
   - Output: the count of non-expired fields across all keys (at time t).

7) ["RESTORE", t, backup_index]
   - Restores the store to exactly the state captured by the given backup
     (0-based index, in the order BACKUPs were created).
   - After restore, current time becomes t (so expiries are evaluated against t
     going forward).
   - Output: "true" if backup_index exists, else "false".

Return value
~~~~~~~~~~~~

Return a list of outputs (strings) for each query that produces output:
GET, DELETE, FIELDS, BACKUP, RESTORE (in order of occurrence).

Hint
~~~~
The hard part is being consistent about expiry across all operations, especially
when combining BACKUP/RESTORE with time moving forward.
"""

from __future__ import annotations


def solution(queries: list[list[str]]) -> list[str]:
    # TODO: implement
    raise NotImplementedError


if __name__ == "__main__":
    sample = [
        ["SET_TTL", "10", "k", "a", "1", "5"],  # expires at 15
        ["GET", "14", "k", "a"],
        ["GET", "15", "k", "a"],
        ["BACKUP", "16"],
    ]
    try:
        print(solution(sample))
    except NotImplementedError:
        import sys

        print("Implement solution() in this file, then run: python3 Verification/verify_04_ttl_backup_store.py", file=sys.stderr)
