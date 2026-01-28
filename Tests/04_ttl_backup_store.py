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
    # store[key][field] = (value, expiry_time_or_None)
    store: dict[str, dict[str, tuple[str, int | None]]] = {}
    backups: list[dict[str, dict[str, tuple[str, int | None]]]] = []
    outputs: list[str] = []
    current_time = 0

    def is_expired(expiry: int | None, now: int) -> bool:
        return expiry is not None and now >= expiry

    def get_entry(key: str, field: str, now: int) -> tuple[str, int | None] | None:
        """Return (value, expiry) if present and not expired; otherwise None. Also prunes expired entries."""
        kd = store.get(key)
        if not kd:
            return None
        entry = kd.get(field)
        if entry is None:
            return None
        val, exp = entry
        if is_expired(exp, now):
            # prune expired
            kd.pop(field, None)
            if not kd:
                store.pop(key, None)
            return None
        return entry

    def prune_key(key: str, now: int) -> None:
        """Remove expired fields for a key (in-place)."""
        kd = store.get(key)
        if not kd:
            return
        expired_fields = [f for f, (_, exp) in kd.items() if is_expired(exp, now)]
        for f in expired_fields:
            kd.pop(f, None)
        if not kd:
            store.pop(key, None)

    for q in queries:
        op = q[0]
        t = int(q[1])
        current_time = t

        if op == "SET":
            _, _, key, field, value = q
            store.setdefault(key, {})[field] = (value, None)

        elif op == "SET_TTL":
            _, _, key, field, value, ttl_s = q
            expiry = current_time + int(ttl_s)
            store.setdefault(key, {})[field] = (value, expiry)

        elif op == "GET":
            _, _, key, field = q
            entry = get_entry(key, field, current_time)
            outputs.append("" if entry is None else entry[0])

        elif op == "DELETE":
            _, _, key, field = q
            entry = get_entry(key, field, current_time)
            if entry is None:
                outputs.append("false")
            else:
                # delete (guaranteed not expired)
                store[key].pop(field, None)
                if not store[key]:
                    store.pop(key, None)
                outputs.append("true")

        elif op == "FIELDS":
            _, _, key = q
            prune_key(key, current_time)
            kd = store.get(key)
            if not kd:
                outputs.append("")
            else:
                items = sorted(((f, v) for f, (v, exp) in kd.items() if not is_expired(exp, current_time)),
                               key=lambda x: x[0])
                outputs.append("" if not items else ",".join(f"{f}={v}" for f, v in items))

        elif op == "BACKUP":
            # Snapshot includes only non-expired fields at time t
            snapshot: dict[str, dict[str, tuple[str, int | None]]] = {}
            count = 0
            # prune expired globally as we walk, to keep store tidy (optional but helpful)
            keys_to_delete: list[str] = []
            for key, kd in store.items():
                new_kd: dict[str, tuple[str, int | None]] = {}
                for field, (val, exp) in kd.items():
                    if not is_expired(exp, current_time):
                        new_kd[field] = (val, exp)
                if new_kd:
                    snapshot[key] = new_kd
                    count += len(new_kd)
                # track keys that became empty due to expiry
                if not new_kd:
                    keys_to_delete.append(key)
            # prune expired-only keys from live store (optional but consistent)
            for key in keys_to_delete:
                # may still have non-expired fields if store changed mid-loop (it won't), but be safe:
                prune_key(key, current_time)

            backups.append(snapshot)
            outputs.append(str(count))

        elif op == "RESTORE":
            _, _, idx_s = q
            idx = int(idx_s)
            if idx < 0 or idx >= len(backups):
                outputs.append("false")
            else:
                # Deep copy snapshot back into store
                snap = backups[idx]
                store = {k: {f: (v, exp) for f, (v, exp) in fields.items()} for k, fields in snap.items()}
                outputs.append("true")

        else:
            raise ValueError(f"Unknown op: {op!r}")

    return outputs


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
