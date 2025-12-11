"""
Utility script to compare SQLite schemas between the legacy
`tribal-knowledge.db` and `myles-tribal-knowledge-2.db`.

Outputs:
- tables present only in one database
- column set and metadata differences for common tables
- CREATE statements for key tables used by test_all_search.py
"""

import sqlite3
import pathlib
from typing import Dict, List, Any

# Load sqlite-vec if available so virtual tables can be inspected
try:
    import sqlite_vec  # type: ignore
except ImportError:
    sqlite_vec = None


BASE = pathlib.Path(__file__).resolve().parent / "data"
DBS = {
    "tribal": BASE / "tribal-knowledge.db",
    "myles2": BASE / "myles-tribal-knowledge-2.db",
}


def get_schema(path: pathlib.Path) -> Dict[str, Dict[str, Any]]:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    if sqlite_vec is not None:
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT name, type, sql FROM sqlite_master "
        "WHERE type IN ('table','view') ORDER BY name"
    ).fetchall()

    schema: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        name = row["name"]
        columns = cur.execute(f"PRAGMA table_info('{name}')").fetchall()
        schema[name] = {
            "type": row["type"],
            "sql": row["sql"],
            "columns": [dict(c) for c in columns],
        }
    conn.close()
    return schema


def diff_tables(a: Dict[str, Any], b: Dict[str, Any]):
    a_set, b_set = set(a), set(b)
    return {
        "only_in_a": sorted(a_set - b_set),
        "only_in_b": sorted(b_set - a_set),
        "both": sorted(a_set & b_set),
    }


def main():
    schemas = {k: get_schema(v) for k, v in DBS.items()}
    diff = diff_tables(schemas["tribal"], schemas["myles2"])

    print("Tables present only in tribal:", diff["only_in_a"])
    print("Tables present only in myles2:", diff["only_in_b"])
    print("Common tables:", len(diff["both"]))
    print()

    print("Column differences for common tables:")
    for name in diff["both"]:
        acols = {c["name"]: c for c in schemas["tribal"][name]["columns"]}
        bcols = {c["name"]: c for c in schemas["myles2"][name]["columns"]}
        if acols.keys() != bcols.keys():
            print(f" {name}:")
            print(f"   tribal-only columns: {sorted(acols.keys() - bcols.keys())}")
            print(f"   myles2-only columns: {sorted(bcols.keys() - acols.keys())}")
            continue
        col_diffs: List[str] = []
        for col in acols:
            ca, cb = acols[col], bcols[col]
            key = ("type", "notnull", "dflt_value", "pk")
            if tuple(ca[k] for k in key) != tuple(cb[k] for k in key):
                col_diffs.append(
                    f"   {col}: tribal={{{'type': ca['type'], 'notnull': ca['notnull'], 'dflt': ca['dflt_value'], 'pk': ca['pk']}}} "
                    f"vs myles2={{{'type': cb['type'], 'notnull': cb['notnull'], 'dflt': cb['dflt_value'], 'pk': cb['pk']}}}"
                )
        if col_diffs:
            print(f" {name}:")
            for line in col_diffs:
                print(line)
    print()

    print("CREATE statements for key tables:")
    for tbl in ("documents", "documents_vec", "documents_fts"):
        if tbl in schemas["tribal"]:
            print(f"-- tribal.{tbl}\n{schemas['tribal'][tbl]['sql']}\n")
        if tbl in schemas["myles2"]:
            print(f"-- myles2.{tbl}\n{schemas['myles2'][tbl]['sql']}\n")


if __name__ == "__main__":
    main()

