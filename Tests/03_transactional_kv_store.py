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
        self.tx_stack: list[dict[str, dict[str, str | None]]] = []

    def setHandler(self, key, field, value):
        if len(self.tx_stack) == 0:
            self.store.setdefault(key, {})[field] = value
            return
        layer = self.tx_stack[-1]
        layer.setdefault(key, {})[field] = value
    
    def getHandler(self, key, field):
        val = self._resolveValue(key, field)
        return "" if val is None else val

    def deleteHandler(self, key, field):
        if self._resolveValue(key, field) is None:
            return "false"

        if len(self.tx_stack) == 0:
            self.store.get(key, {}).pop(field, None)
            if key in self.store and len(self.store[key]) == 0:
                self.store.pop(key, None)
            return "true"

        layer = self.tx_stack[-1]
        layer.setdefault(key, {})[field] = None
        return "true"

    def fieldsHandler(self, key):
        view = dict(self.store.get(key, {}))

        for layer in self.tx_stack:
            if key not in layer:
                continue
            for field, value in layer[key].items():
                if value is None:
                    view.pop(field, None)
                else:
                    view[field] = value

        if len(view) == 0:
            return ""
        items = sorted(view.items(), key=lambda kv: kv[0])
        return ",".join(f"{field}={value}" for field, value in items)

    def beginHandler(self):
        self.tx_stack.append({})

    def commitHandler(self):
        if len(self.tx_stack) == 0:
            return "false"

        top = self.tx_stack.pop()
        if len(self.tx_stack) > 0:
            parent = self.tx_stack[-1]
            for key, fields in top.items():
                parent_fields = parent.setdefault(key, {})
                for field, value in fields.items():
                    parent_fields[field] = value
        else:
            for key, fields in top.items():
                for field, value in fields.items():
                    if value is None:
                        if key in self.store:
                            self.store[key].pop(field, None)
                            if len(self.store[key]) == 0:
                                self.store.pop(key, None)
                    else:
                        self.store.setdefault(key, {})[field] = value

        return "true"

    def rollbackHandler(self):
        if len(self.tx_stack) == 0:
            return "false"
        self.tx_stack.pop()
        return "true"

    def _resolveValue(self, key: str, field: str) -> str | None:
        for layer in reversed(self.tx_stack):
            if key not in layer:
                continue
            if field not in layer[key]:
                continue
            return layer[key][field]
        return self.store.get(key, {}).get(field)

    

def solution(queries: list[list[str]]) -> list[str]:
    db = Database()
    outputs = []
    for query in queries:
        queryType, key, field, value = (query+ [None, None, None, None])[:4]

        if queryType == "SET":
            db.setHandler(key, field, value)
        elif queryType == "GET":
            outputs.append(db.getHandler(key, field))
        elif queryType == "DELETE":
            outputs.append(db.deleteHandler(key, field))
        elif queryType == "FIELDS":
            outputs.append(db.fieldsHandler(key))
        elif queryType == "BEGIN":
            db.beginHandler()
        elif queryType == "COMMIT":
            outputs.append(db.commitHandler())
        elif queryType == "ROLLBACK":
            outputs.append(db.rollbackHandler())
        else:
            raise ValueError(f"Unknown query type: {queryType!r}")
    return outputs


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
