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
        self.store: dict[str, dict[str, str]] = {}
    
    def setHandler(self, key, field, value):
        try:
            self.store[key](field, value)
        except KeyError:
            self.store[key] = {}
            self.store[key].setdefault(field, value)
    
    def getHandler(self, key, field):
        return self.store.get(key, {}).get(field, "")

    def deleteHandler(self, key, field):
        value = self.getHandler(key, field)
        if value == "":
            return "false"
        remove = self.store[key].pop(field)
        return "true"

    def fieldsHandler(self, key):
        if key not in self.store:
            print("")
        elif self.store[key] is not None:
            fields = []
            for fieldDict in self.store[key].keys():
                fields.append(fieldDict)
            fields.sort(key=lambda x: x[0])
            for field in fields:
                field.join("=")
            print(",".join(fields))
        else:
            raise ValueError(f"Key {key!r} not found")

    def beginHandler(self):
        pass

    def commitHandler(self):
        pass

    def rollbackHandler(self):
        pass

    

def solution(queries: list[list[str]]) -> list[str]:
    db = Database()
    for query in queries:
        queryType, key, field, value = (query+ [None, None, None, None])[:4]

        if queryType == "SET":
            db.setHandler(key, field, value)
        elif queryType == "GET":
            db.getHandler(key, field)
        elif queryType == "DELETE":
            db.deleteHandler(key, field)
        elif queryType == "FIELDS":
            db.fieldsHandler(key)
        elif queryType == "BEGIN":
            db.beginHandler()
        elif queryType == "COMMIT":
            db.commitHandler()
        elif queryType == "ROLLBACK":
            db.rollbackHandler()
        else:
            raise ValueError(f"Unknown query type: {queryType!r}")
    raise NotImplementedError


if __name__ == "__main__":
    sample = [
        ["SET", "u1", "name", "tom"],
        ["BEGIN"],
        ["SET", "u1", "name", "tom2"],
        ["SET", "u2", "name", "tom2"],
        ["DELETE", "u1", "name"],
        ["GET", "u1", "name"],
        ]
    print(solution(sample))

""" 
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
"""