"""
data_router.py  -  Decree 53 Data Localization Middleware
==========================================================
Classifies every GQL request into one of four categories:

  user_profile   -> Local_DB  (MySQL, Vietnam)   [Decree 53 §17]
  ip_log         -> Local_DB  (MySQL, Vietnam)   [Decree 53 §17]
  app_metadata   -> Global_DB (Apollo/PostgreSQL) [no restriction]
  image_cache    -> Global_DB (Apollo/PostgreSQL) [no restriction]

Rules:
  - ip_log      : written for EVERY request regardless of category
  - user_profile mutation : additionally writes a payload snapshot to user_profile_audit
  - app_metadata / image_cache : forwarded only, nothing written to Local_DB

Environment variables (set in docker-compose):
  LOCAL_DB_HOST      default: local_mysql
  LOCAL_DB_PORT      default: 3306
  LOCAL_DB_USER      default: root
  LOCAL_DB_PASSWORD  default: localpass
  LOCAL_DB_NAME      default: local_db
"""

import re
import json
import uuid
import logging
import os
from datetime import datetime
from typing import Optional, Dict

import aiomysql

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Classification patterns
# Priority order: user_profile > image_cache > app_metadata
# ---------------------------------------------------------------------------

_USER_PROFILE_RE = re.compile(
    r'\b(user|users|userPage|userById|userInsert|userUpdate|userDelete'
    r'|group|groups|groupPage|groupById|groupInsert|groupUpdate|groupDelete'
    r'|membership|memberships|membershipPage|membershipInsert|membershipUpdate'
    r'|role|roles|rolePage|roleInsert|roleUpdate|roleDelete'
    r'|roletype|roletypes|roleTypePage'
    r'|grouptype|grouptypes|groupTypePage)\b',
    re.IGNORECASE,
)

_IMAGE_CACHE_RE = re.compile(
    r'\b(image|images|avatar|photo|thumbnail|blob|file|cache|attachment)\b',
    re.IGNORECASE,
)

_MUTATION_RE = re.compile(r'^\s*mutation\b', re.IGNORECASE | re.MULTILINE)
_OPERATION_NAME_RE = re.compile(r'(?:mutation|query|subscription)\s+(\w+)', re.IGNORECASE)


def classify_payload(query: str) -> str:
    """
    Returns one of: 'user_profile', 'image_cache', 'app_metadata'.
    If a query contains both user and event/app fields, user_profile wins.
    Routing is per-request, not per-field.
    """
    if not query:
        return "app_metadata"
    if _USER_PROFILE_RE.search(query):
        return "user_profile"
    if _IMAGE_CACHE_RE.search(query):
        return "image_cache"
    return "app_metadata"


def is_mutation(query: str) -> bool:
    return bool(_MUTATION_RE.search(query or ""))


def extract_operation_name(query: str) -> Optional[str]:
    m = _OPERATION_NAME_RE.search(query or "")
    return m.group(1) if m else None


# ---------------------------------------------------------------------------
# MySQL connection pool
# ---------------------------------------------------------------------------

_pool: Optional[aiomysql.Pool] = None


async def get_pool() -> Optional[aiomysql.Pool]:
    """Return the shared pool, creating it lazily if needed. Returns None on failure."""
    global _pool
    if _pool is None:
        try:
            _pool = await aiomysql.create_pool(
                host=os.getenv("LOCAL_DB_HOST", "local_mysql"),
                port=int(os.getenv("LOCAL_DB_PORT", "3306")),
                user=os.getenv("LOCAL_DB_USER", "root"),
                password=os.getenv("LOCAL_DB_PASSWORD", "localpass"),
                db=os.getenv("LOCAL_DB_NAME", "local_db"),
                autocommit=True,
                charset="utf8mb4",
            )
            logger.info("[Decree53] Connected to Local_DB (MySQL)")
        except Exception as e:
            logger.error(f"[Decree53] Cannot connect to Local_DB: {e}")
            return None
    return _pool


async def init_pool() -> bool:
    """
    Explicitly initialize the pool at FastAPI startup.
    Returns True if the connection is healthy.
    """
    pool = await get_pool()
    if pool is None:
        return False
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
        logger.info("[Decree53] Local_DB ready")
        return True
    except Exception as e:
        logger.error(f"[Decree53] Local_DB connectivity check failed: {e}")
        return False


async def close_pool():
    global _pool
    if _pool:
        _pool.close()
        await _pool.wait_closed()
        _pool = None
        logger.info("[Decree53] Local_DB pool closed")


# ---------------------------------------------------------------------------
# Write helpers
# ---------------------------------------------------------------------------

async def _run(sql: str, params: tuple):
    """Execute a single INSERT against Local_DB. Silently skips if DB is unavailable."""
    pool = await get_pool()
    if pool is None:
        return
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(sql, params)
    except Exception as e:
        logger.error(f"[Decree53] DB write failed: {e}")


async def _write_ip_log(ip: str, endpoint: str, method: str, user_agent: str,
                        user_id: Optional[str], operation: Optional[str],
                        status: int, category: str):
    await _run(
        "INSERT INTO ip_logs "
        "(id, user_id, ip_address, endpoint, method, user_agent, gql_operation, status_code, data_category, ts) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (str(uuid.uuid4()), user_id, ip[:45], endpoint[:512], method[:10],
         (user_agent or "")[:512], (operation or "")[:255],
         status, category[:50], datetime.utcnow()),
    )


async def _write_audit(query: str, variables: Optional[Dict],
                       user_id: Optional[str], operation: Optional[str]):
    payload = json.dumps(
        {"query": query[:2000], "variables": variables or {}},
        ensure_ascii=False,
    )
    await _run(
        "INSERT INTO user_profile_audit (id, user_id, operation_name, payload, recorded_at) "
        "VALUES (%s,%s,%s,%s,%s)",
        (str(uuid.uuid4()), user_id, (operation or "")[:255], payload, datetime.utcnow()),
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class DataRouter:
    @staticmethod
    async def process(query: str, variables: Optional[Dict],
                      request_ip: str, endpoint: str, method: str,
                      user_agent: str, user_id: Optional[str],
                      status_code: int = 200) -> str:
        """
        Main entry point. Called once per GQL request after the upstream response.
        Returns the data_category string used in response headers.
        """
        category = classify_payload(query)
        operation = extract_operation_name(query)

        # Always write ip_log
        await _write_ip_log(request_ip, endpoint, method, user_agent,
                            user_id, operation, status_code, category)

        # Write audit snapshot only for user_profile mutations
        if category == "user_profile" and is_mutation(query):
            await _write_audit(query, variables, user_id, operation)

        logger.info(
            f"[Decree53] {method} {endpoint} ip={request_ip} "
            f"category={category} op={operation} routed={'local' if category == 'user_profile' else 'global'}"
        )
        return category
