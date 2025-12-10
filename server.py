from fastmcp import FastMCP
import re
from collections import defaultdict
from typing import List, Dict, Any, DefaultDict, Set

# Minimal FastMCP server with a couple of example tools.
mcp = FastMCP("Example Server")

# --- Context map data (manually curated from _docs/map) ---
DB_SEGMENTS: List[Dict[str, Any]] = [
    {
        "id": "dabstep_tasks",
        "title": "dabstep_tasks table",
        "summary": "Task definitions with difficulty level and optional question/answer/guidelines.",
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


def _normalize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _build_index(segments: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
    """
    Build a lightweight inverted index: token -> set(segment_ids).
    Scales better as the context map grows.
    """
    index: DefaultDict[str, Set[str]] = defaultdict(set)
    for seg in segments:
        text_parts = [
            seg.get("id", ""),
            seg.get("title", ""),
            seg.get("summary", ""),
            " ".join(col["name"] for col in seg.get("columns", [])),
        ]
        for token in _normalize(" ".join(text_parts)):
            index[token].add(seg["id"])
    return dict(index)


INDEX = _build_index(DB_SEGMENTS)


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


if __name__ == "__main__":
    # Bind to 0.0.0.0 for container networking; use HTTP transport for remote access.
    mcp.run(transport="http", host="0.0.0.0", port=8000)

