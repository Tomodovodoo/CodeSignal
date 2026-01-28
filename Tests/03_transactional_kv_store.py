"""
3. Transactional Key/Field Store
--------------------------------

Implement an in-memory key -> field -> value store with nested transactions.

You are given a list of queries. Each query is a list of strings.

Write:
    solution(queries: list[list[str]]) -> list[str]

Data model
~~~~~~~~~~

The store maps:
    key (string) -> field (string) -> value (string)

Queries
~~~~~~~

Core operations:

1) ["SET", key, field, value]
   - Sets key.field = value (overwriting if present).
   - Output: none.

2) ["GET", key, field]
   - Output: value, or "" (empty string) if missing.

3) ["DELETE", key, field]
   - Deletes the field if present.
   - Output: "true" if deleted, else "false".

4) ["FIELDS", key]
   - Output a comma-separated list of "field=value" pairs.
   - Include only fields currently present for the key.
   - Sort fields lexicographically by field name.
   - If the key has no fields, output "".

Transactions:

5) ["BEGIN"]
   - Starts a new (possibly nested) transaction. Output: none.

6) ["COMMIT"]
   - Commits the most recent transaction.
   - Output: "true" if a transaction was committed, else "false".

7) ["ROLLBACK"]
   - Rolls back (undoes) the most recent transaction.
   - Output: "true" if a transaction was rolled back, else "false".

Semantics
~~~~~~~~~

 - Reads always reflect the latest uncommitted changes.
 - Nested transactions are supported.
 - COMMIT merges changes into the parent transaction (or base state).
 - ROLLBACK restores the state as it was at the matching BEGIN.

Return value
~~~~~~~~~~~~

Return a list of outputs (strings) for each query that produces output:
GET, DELETE, FIELDS, COMMIT, ROLLBACK (in order of occurrence).
"""

from __future__ import annotations

class Database:
    def __init__(self):
        self.store = {}
    
    def setHandler(self, key, field, value):
        self.store[key] = {field: value}

    def getHandler(self, key, field):
        if self.store[key][field] is None:
            print("")
        elif self.store[key][field] is not None:
            print(self.store[key][field])
        else:
            raise ValueError(f"Key {key!r} or field {field!r} not found")

    def deleteHandler(self, key, field):
        pass

    def fieldsHandler(self, key):
        pass

    def beginHandler(self):
        pass

    def commitHandler(self):
        pass

    def rollbackHandler(self):
        pass

    

def solution(queries: list[list[str]]) -> list[str]:
    for query in queries:
        queryType, key, field, value = (query+ [None, None, None, None])[:4]

        if queryType == "SET":
            Database.setHandler(key, field, value)
        elif queryType == "GET":
            Database.getHandler(key, field)
        elif queryType == "DELETE":
            Database.deleteHandler(key, field)
        elif queryType == "FIELDS":
            Database.fieldsHandler(key)
        elif queryType == "BEGIN":
            Database.beginHandler()
        elif queryType == "COMMIT":
            Database.commitHandler()
        elif queryType == "ROLLBACK":
            Database.rollbackHandler()
        else:
            raise ValueError(f"Unknown query type: {queryType!r}")
    raise NotImplementedError


if __name__ == "__main__":
    sample = [
        ["SET", "u1", "name", "tom"],
        ["BEGIN"],
        ["SET", "u1", "name", "tom2"],
        ["GET", "u1", "name"],
        ["ROLLBACK"],
        ["GET", "u1", "name"],
    ]
    try:
        print(solution(sample))
    except NotImplementedError:
        import sys

        print(
            "Implement solution() in this file, then run: python3 Verification/verify_03_transactional_kv_store.py",
            file=sys.stderr,
        )
