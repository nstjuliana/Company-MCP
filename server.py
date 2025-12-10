from fastmcp import FastMCP
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import List, Dict, Any, DefaultDict, Set

# Minimal FastMCP server with a couple of example tools.
mcp = FastMCP("Example Server")

BASE_DIR = Path(__file__).resolve().parent
CONTEXT_MAP_PATH = BASE_DIR / "_docs" / "map" / "context_map.json"
CONTEXT_INDEX_PATH = BASE_DIR / "_docs" / "map" / "context_index.json"

# Fallback context map so the server stays functional if JSON is missing or empty.
DEFAULT_CONTEXT_MAP: List[Dict[str, Any]] = [
    {
        "id": "dabstep_tasks",
        "title": "dabstep_tasks table",
        "summary": "Task definitions with difficulty level and optional question/answer/guidelines.",
        "database": "default",
        "domain": "tasks",
        "columns": [
            {"name": "TASK_ID", "type": "integer", "notes": "primary key"},
            {"name": "QUESTION", "type": "text", "notes": "nullable"},
            {"name": "ANSWER", "type": "text", "notes": "nullable"},
            {"name": "GUIDELINES", "type": "text", "notes": "nullable"},
            {"name": "LEVEL", "type": "text", "notes": "not null, e.g., easy/hard"},
        ],
        "keys": {
            "primary": ["TASK_ID"],
            "checks": ["LEVEL in ('easy','hard') (optional)"],
        },
        "relationships": {"referenced_by": ["dabstep_submissions.TASK_ID", "dabstep_task_scores.TASK_ID"]},
    },
    {
        "id": "dabstep_submissions",
        "title": "dabstep_submissions table",
        "summary": "Stores agent submissions per task with metadata and validation status.",
        "database": "default",
        "domain": "tasks",
        "columns": [
            {"name": "TASK_ID", "type": "integer", "notes": "FK -> dabstep_tasks.TASK_ID"},
            {"name": "AGENT_ANSWER", "type": "text", "notes": "nullable"},
            {"name": "SUBMISSION_ID", "type": "text", "notes": "primary key"},
            {"name": "AGENT_NAME", "type": "text", "notes": "not null"},
            {"name": "MODEL_FAMILY", "type": "integer", "notes": "not null"},
            {"name": "ORGANISATION", "type": "text", "notes": "nullable"},
            {"name": "REPO_URL", "type": "text", "notes": "nullable"},
            {"name": "DATE", "type": "text", "notes": "dd-mm-yyyy in sample"},
            {"name": "VALIDATED", "type": "boolean", "notes": "not null"},
        ],
        "keys": {
            "primary": ["SUBMISSION_ID"],
            "foreign": [{"columns": ["TASK_ID"], "references": "dabstep_tasks(TASK_ID)"}],
            "unique_optional": ["(TASK_ID, AGENT_NAME, ORGANISATION) to prevent duplicates"],
        },
        "relationships": {
            "depends_on": ["dabstep_tasks"],
            "referenced_by": ["dabstep_task_scores.SUBMISSION_ID"],
        },
    },
    {
        "id": "dabstep_task_scores",
        "title": "dabstep_task_scores table",
        "summary": "Scores for submissions per task, with level and optional agent answer copy.",
        "database": "default",
        "domain": "tasks",
        "columns": [
            {"name": "SUBMISSION_ID", "type": "text", "notes": "FK -> dabstep_submissions.SUBMISSION_ID"},
            {"name": "TASK_ID", "type": "integer", "notes": "FK -> dabstep_tasks.TASK_ID"},
            {"name": "SCORE", "type": "boolean", "notes": "not null"},
            {"name": "LEVEL", "type": "text", "notes": "not null, aligns with tasks"},
            {"name": "AGENT_ANSWER", "type": "text", "notes": "nullable"},
        ],
        "keys": {
            "primary": ["SUBMISSION_ID", "TASK_ID"],
            "foreign": [
                {"columns": ["SUBMISSION_ID"], "references": "dabstep_submissions(SUBMISSION_ID)"},
                {"columns": ["TASK_ID"], "references": "dabstep_tasks(TASK_ID)"},
            ],
        },
        "relationships": {"depends_on": ["dabstep_submissions", "dabstep_tasks"]},
    },
    {
        "id": "dabstep_payments",
        "title": "dabstep_payments table",
        "summary": "Payment events with merchant, card, timing, and fraud/refusal indicators.",
        "database": "default",
        "domain": "payments",
        "columns": [
            {"name": "PSP_REFERENCE", "type": "bigint", "notes": "primary key"},
            {"name": "MERCHANT", "type": "text", "notes": "not null"},
            {"name": "CARD_SCHEME", "type": "text", "notes": "not null"},
            {"name": "YEAR", "type": "integer", "notes": "not null"},
            {"name": "HOUR_OF_DAY", "type": "integer", "notes": "0-23"},
            {"name": "MINUTE_OF_HOUR", "type": "integer", "notes": "0-59"},
            {"name": "DAY_OF_YEAR", "type": "integer", "notes": "1-366"},
            {"name": "IS_CREDIT", "type": "boolean", "notes": "not null"},
            {"name": "EUR_AMOUNT", "type": "numeric", "notes": "currency amount"},
            {"name": "IP_COUNTRY", "type": "text", "notes": "2-letter"},
            {"name": "ISSUING_COUNTRY", "type": "text", "notes": "2-letter"},
            {"name": "DEVICE_TYPE", "type": "text", "notes": ""},
            {"name": "IP_ADDRESS", "type": "text", "notes": ""},
            {"name": "EMAIL_ADDRESS", "type": "text", "notes": ""},
            {"name": "CARD_NUMBER", "type": "text", "notes": ""},
            {"name": "SHOPPER_INTERACTION", "type": "text", "notes": "e.g., Ecommerce"},
            {"name": "CARD_BIN", "type": "integer", "notes": ""},
            {"name": "HAS_FRAUDULENT_DISPUTE", "type": "boolean", "notes": "not null"},
            {"name": "IS_REFUSED_BY_ADYEN", "type": "boolean", "notes": "not null"},
            {"name": "ACI", "type": "text", "notes": "single-letter code"},
            {"name": "ACQUIRER_COUNTRY", "type": "text", "notes": "2-letter"},
        ],
        "keys": {
            "primary": ["PSP_REFERENCE"],
            "checks": [
                "HOUR_OF_DAY between 0 and 23",
                "MINUTE_OF_HOUR between 0 and 59",
                "DAY_OF_YEAR between 1 and 366",
            ],
            "pii_columns": ["EMAIL_ADDRESS", "CARD_NUMBER", "IP_ADDRESS"],
        },
        "relationships": {"depends_on": []},
    },
]


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _safe_load_map() -> List[Dict[str, Any]]:
    try:
        data = _load_json(CONTEXT_MAP_PATH)
        if isinstance(data, list) and data:
            return data
    except FileNotFoundError:
        pass
    except Exception:
        pass
    # Fallback to embedded defaults if file missing or empty.
    return DEFAULT_CONTEXT_MAP.copy()


DB_SEGMENTS: List[Dict[str, Any]] = _safe_load_map()


def _normalize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _segment_tokens(seg: Dict[str, Any]) -> Set[str]:
    text_parts = [
        seg.get("id", ""),
        seg.get("title", ""),
        seg.get("summary", ""),
        seg.get("database", ""),
        seg.get("domain", ""),
        " ".join(col.get("name", "") for col in seg.get("columns", [])),
    ]
    return set(_normalize(" ".join(text_parts)))


def _build_index(segments: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
    """
    Build a lightweight inverted index: token -> set(segment_ids).
    Scales better as the context map grows.
    """
    index: DefaultDict[str, Set[str]] = defaultdict(set)
    for seg in segments:
        for token in _segment_tokens(seg):
            index[token].add(seg["id"])
    return dict(index)


def _safe_load_index() -> Dict[str, Set[str]]:
    try:
        data = _load_json(CONTEXT_INDEX_PATH)
        if isinstance(data, dict):
            return {token: set(ids) for token, ids in data.items()}
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return _build_index(DB_SEGMENTS)


INDEX = _safe_load_index()
SEGMENT_BY_ID: Dict[str, Dict[str, Any]] = {seg["id"]: seg for seg in DB_SEGMENTS}


def _find_table(table: str) -> Dict[str, Any]:
    table_norm = table.lower()
    for seg in DB_SEGMENTS:
        if seg["id"].lower() == table_norm or seg.get("title", "").lower() == table_norm:
            return seg
    return {}


def _estimate_tokens(text: str) -> int:
    # Rough heuristic: 1 token ≈ 4 chars; sufficient for budget hints.
    return max(1, len(text) // 4)


def _foreign_key_edges(seg: Dict[str, Any]) -> List[Dict[str, Any]]:
    edges = []
    for fk in seg.get("keys", {}).get("foreign", []) or []:
        ref = fk.get("references", "")
        ref_table = ref.split("(")[0] if "(" in ref else ref
        edges.append(
            {
                "from": seg["id"],
                "to": ref_table,
                "columns": fk.get("columns", []),
                "references": ref,
            }
        )
    return edges


def _build_graph() -> Dict[str, List[Dict[str, Any]]]:
    graph: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)
    for seg in DB_SEGMENTS:
        # Foreign key edges (bidirectional for traversal)
        for edge in _foreign_key_edges(seg):
            graph[edge["from"]].append({"to": edge["to"], "info": edge})
            graph[edge["to"]].append({"to": edge["from"], "info": edge})
        rel = seg.get("relationships", {}) or {}
        for dep in rel.get("depends_on", []) or []:
            graph[seg["id"]].append({"to": dep, "info": {"note": "depends_on"}})
            graph[dep].append({"to": seg["id"], "info": {"note": "referenced_by"}})
        for ref in rel.get("referenced_by", []) or []:
            graph[seg["id"]].append({"to": ref, "info": {"note": "referenced_by"}})
            graph[ref].append({"to": seg["id"], "info": {"note": "depends_on"}})
    return graph


GRAPH = _build_graph()


@mcp.tool
def add(a: float, b: float) -> float:
    """Add two numbers to verify tool execution."""
    return a + b


@mcp.tool
def echo(message: str) -> str:
    """Echo a message to confirm connectivity."""
    return message


@mcp.tool
def search_db_map(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Match a natural language query to the most relevant DB map segments.
    Returns top_k segments with id, title, score, and snippet.
    """
    q_tokens = set(_normalize(query))
    candidate_ids: Set[str] = set()

    # Retrieve candidate segment ids via inverted index for efficiency.
    for token in q_tokens:
        candidate_ids |= INDEX.get(token, set())

    # Fallback: if no candidates, consider all segments.
    if not candidate_ids:
        candidate_ids = {seg["id"] for seg in DB_SEGMENTS}

    scored = []
    for seg in DB_SEGMENTS:
        if seg["id"] not in candidate_ids:
            continue
        text_parts = [
            seg.get("id", ""),
            seg.get("title", ""),
            seg.get("summary", ""),
            " ".join(col["name"] for col in seg.get("columns", [])),
        ]
        seg_tokens = set(_normalize(" ".join(text_parts)))
        score = len(q_tokens & seg_tokens)
        scored.append(
            {
                "id": seg["id"],
                "title": seg["title"],
                "score": score,
                "snippet": seg["summary"],
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[: max(1, top_k)]


@mcp.resource("resource://db-map")
def db_map() -> Dict[str, Any]:
    """Full database context map."""
    return {"segments": DB_SEGMENTS, "index_tokens": sorted(list(INDEX.keys()))}


@mcp.resource("resource://db-map/{segment_id}")
def db_map_segment(segment_id: str) -> Dict[str, Any]:
    """Fetch a single segment by id."""
    for seg in DB_SEGMENTS:
        if seg["id"] == segment_id:
            return seg
    return {"error": f"segment '{segment_id}' not found"}


@mcp.resource("resource://db-map-index")
def db_map_index() -> Dict[str, Any]:
    """
    Expose the inverted index so clients can inspect token->segment mappings.
    Useful for debugging and future smarter retrieval strategies.
    """
    return {"index": {token: sorted(list(ids)) for token, ids in INDEX.items()}}


# --- PRD2 tools based on planning spec ---


@mcp.tool
def list_tables(database: str = "", domain: str = "") -> List[Dict[str, Any]]:
    """List available tables, optionally filtered by database or domain."""
    results = []
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        if domain and seg.get("domain", "") != domain:
            continue
        results.append(
            {
                "name": seg["id"],
                "title": seg.get("title", seg["id"]),
                "database": seg.get("database", "default"),
                "domain": seg.get("domain", "default"),
                "summary": seg.get("summary", ""),
                "key_columns": seg.get("keys", {}).get("primary", []),
            }
        )
    return results


@mcp.tool
def list_columns(table: str) -> Dict[str, Any]:
    """List columns for a given table id/title."""
    seg = _find_table(table)
    if not seg:
        return {"error": f"table '{table}' not found"}
    columns = []
    for col in seg.get("columns", []):
        columns.append(
            {
                "name": col.get("name"),
                "type": col.get("type"),
                "nullable": "not null" not in (col.get("notes", "") or "").lower(),
                "description": col.get("notes", ""),
            }
        )
    return {"table": seg["id"], "columns": columns}


@mcp.tool
def search_tables(
    query: str, database: str = "", domain: str = "", limit: int = 5
) -> Dict[str, Any]:
    """
    Find tables relevant to a natural language query.
    Simplified implementation using token overlap on the curated map.
    """
    limit = max(1, min(limit, 20))
    q_tokens = set(_normalize(query))
    scored = []
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        if domain and seg.get("domain", "") != domain:
            continue
        seg_tokens = _segment_tokens(seg)
        overlap = len(q_tokens & seg_tokens)
        # Light boost for substring matches in id/title/summary.
        text_blob = " ".join(
            [seg.get("id", ""), seg.get("title", ""), seg.get("summary", "")]
        ).lower()
        if any(tok in text_blob for tok in q_tokens):
            overlap += 0.5
        scored.append(
            {
                "name": seg["id"],
                "database": seg.get("database", "default"),
                "domain": seg.get("domain", "default"),
                "summary": seg.get("summary", ""),
                "key_columns": seg.get("keys", {}).get("primary", []),
                "relevance_score": round(overlap, 3),
            }
        )

    scored.sort(key=lambda x: x["relevance_score"], reverse=True)
    results = scored[:limit]
    return {
        "tables": results,
        "tokens_used": _estimate_tokens(query),
        "total_matches": len(scored),
    }


@mcp.tool
def get_table_schema(table: str, include_samples: bool = False) -> Dict[str, Any]:
    """Retrieve full schema details for a specific table."""
    seg = _find_table(table)
    if not seg:
        return {"error": f"table '{table}' not found"}

    columns = []
    for col in seg.get("columns", []):
        col_entry = {
            "name": col.get("name"),
            "type": col.get("type"),
            "nullable": "not null" not in (col.get("notes", "") or "").lower(),
            "description": col.get("notes", ""),
        }
        if include_samples:
            col_entry["samples"] = []
        columns.append(col_entry)

    keys = seg.get("keys", {}) or {}
    foreign_keys = []
    for fk in keys.get("foreign", []) or []:
        ref = fk.get("references", "")
        ref_table = ref.split("(")[0] if "(" in ref else ref
        foreign_keys.append(
            {"columns": fk.get("columns", []), "references": ref, "table": ref_table}
        )

    return {
        "name": seg["id"],
        "database": seg.get("database", "default"),
        "schema": seg.get("schema", "public"),
        "description": seg.get("summary", ""),
        "row_count": seg.get("row_count"),
        "columns": columns,
        "primary_key": keys.get("primary", []),
        "foreign_keys": foreign_keys,
        "indexes": keys.get("indexes", []),
        "related_tables": seg.get("relationships", {}),
        "tokens_used": _estimate_tokens(seg.get("summary", "")),
    }


@mcp.tool
def get_join_path(
    source_table: str, target_table: str, max_hops: int = 3
) -> Dict[str, Any]:
    """
    Find the join path between two tables using relationship graph traversal.
    """
    src = _find_table(source_table).get("id")
    tgt = _find_table(target_table).get("id")
    if not src or not tgt:
        return {"error": "source or target table not found"}

    visited = {src}
    queue = deque([(src, [])])
    found_path: List[str] = []

    while queue:
        node, path = queue.popleft()
        if len(path) > max_hops:
            continue
        if node == tgt:
            found_path = path
            break
        for edge in GRAPH.get(node, []):
            nxt = edge["to"]
            if nxt in visited:
                continue
            visited.add(nxt)
            queue.append((nxt, path + [edge]))

    if not found_path:
        return {
            "source": src,
            "target": tgt,
            "found": False,
            "hop_count": None,
            "path": [],
            "sql_snippet": None,
            "tokens_used": _estimate_tokens(source_table + target_table),
        }

    path_steps = []
    joins = []
    prev = src
    for step in found_path:
        nxt = step["to"]
        info = step.get("info", {})
        on_clause = info.get("references", info.get("note", ""))
        join_type = "inner"
        path_steps.append(
            {"from_table": prev, "to_table": nxt, "join_type": join_type, "on_clause": on_clause}
        )
        joins.append(f"JOIN {nxt} ON {on_clause or '/* specify join condition */'}")
        prev = nxt

    sql_snippet = f"SELECT * FROM {src} " + " ".join(joins)
    return {
        "source": src,
        "target": tgt,
        "found": True,
        "hop_count": len(path_steps),
        "path": path_steps,
        "sql_snippet": sql_snippet,
        "tokens_used": _estimate_tokens(sql_snippet),
    }


@mcp.tool
def get_domain_overview(domain: str, database: str = "") -> Dict[str, Any]:
    """Get summary of all tables in a business domain."""
    tables = []
    for seg in DB_SEGMENTS:
        if domain and seg.get("domain", "") != domain:
            continue
        if database and seg.get("database", "") != database:
            continue
        tables.append(
            {
                "name": seg["id"],
                "description": seg.get("summary", ""),
                "row_count": seg.get("row_count"),
            }
        )

    return {
        "domain": domain or "default",
        "description": f"Overview for domain '{domain or 'default'}'",
        "databases": sorted({seg.get("database", "default") for seg in DB_SEGMENTS}),
        "tables": tables,
        "er_diagram": None,
        "common_joins": [],
        "tokens_used": _estimate_tokens(domain),
    }


@mcp.tool
def list_domains(database: str = "") -> Dict[str, Any]:
    """List all available business domains."""
    domains: DefaultDict[str, Dict[str, Any]] = defaultdict(
        lambda: {"name": "", "description": "", "table_count": 0, "databases": set()}
    )
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        dom = seg.get("domain", "default")
        domains[dom]["name"] = dom
        domains[dom]["description"] = f"Tables under domain '{dom}'"
        domains[dom]["table_count"] += 1
        domains[dom]["databases"].add(seg.get("database", "default"))

    return {
        "domains": [
            {
                "name": dom["name"],
                "description": dom["description"],
                "table_count": dom["table_count"],
                "databases": sorted(list(dom["databases"])),
            }
            for dom in domains.values()
        ],
        "tokens_used": _estimate_tokens(database),
    }


@mcp.tool
def get_common_relationships(
    database: str = "", domain: str = "", limit: int = 10
) -> Dict[str, Any]:
    """Retrieve frequently used join patterns based on foreign keys."""
    limit = max(1, limit)
    relationships = []
    for seg in DB_SEGMENTS:
        if database and seg.get("database", "") != database:
            continue
        if domain and seg.get("domain", "") != domain:
            continue
        for fk in seg.get("keys", {}).get("foreign", []) or []:
            ref = fk.get("references", "")
            ref_table = ref.split("(")[0] if "(" in ref else ref
            join_sql = f"{seg['id']} JOIN {ref_table} ON {ref}"
            relationships.append(
                {
                    "source_table": seg["id"],
                    "target_table": ref_table,
                    "join_sql": join_sql,
                    "description": "Foreign key relationship",
                }
            )

    return {"relationships": relationships[:limit], "tokens_used": _estimate_tokens(database + domain)}


if __name__ == "__main__":
    # Bind to 0.0.0.0 for container networking; use HTTP transport for remote access.
    mcp.run(transport="http", host="0.0.0.0", port=8000)

