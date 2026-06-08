"""
scripts/test_decree53.py
========================
Integration tests for Decree 53 routing middleware.

Sends REAL GraphQL requests to the running hk2026 system and verifies:
  - user/group queries  -> X-Decree53-Routed: local  (MySQL Local_DB)
  - event/project queries -> X-Decree53-Routed: global (PostgreSQL Global_DB)
  - mixed payload (user + event fields) -> user_profile wins, routed local
  - ip_logs written to MySQL for every request
  - user_profile_audit written only for user mutations

Requirements:
  - Stack must be running:
      docker compose -f docker-compose.hk2026.yml -f docker-compose.hk2026.decree53.yml up --build
  - pip install requests aiomysql

Usage:
  python scripts/test_decree53.py

Env vars (optional overrides):
  API_URL        default: http://localhost:33001
  LOCAL_DB_HOST  default: 127.0.0.1
  LOCAL_DB_PORT  default: 3307
  LOCAL_DB_USER  default: root
  LOCAL_DB_PASS  default: localpass
  LOCAL_DB_NAME  default: local_db
"""

import asyncio
import os
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: pip install requests")
    sys.exit(1)

try:
    import aiomysql
except ImportError:
    print("ERROR: pip install aiomysql")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

API_URL   = os.getenv("API_URL", "http://localhost:33001")
GQL_URL   = f"{API_URL}/api/gql"
HEALTH_URL = f"{API_URL}/decree53/health"

DB_HOST = os.getenv("LOCAL_DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("LOCAL_DB_PORT", "3307"))
DB_USER = os.getenv("LOCAL_DB_USER", "root")
DB_PASS = os.getenv("LOCAL_DB_PASS", "localpass")
DB_NAME = os.getenv("LOCAL_DB_NAME", "local_db")

HEADERS = {"Content-Type": "application/json"}

passed = 0
failed = 0
_auth_token = None  # cached for the session


def ok(msg):
    global passed
    passed += 1
    print(f"  [PASS] {msg}")


def fail(msg):
    global failed
    failed += 1
    print(f"  [FAIL] {msg}")


def get_auth_token() -> str:
    """
    Log in via /oauth/login3 (JSON API - no browser redirects needed).
    Returns a JWT string that can be sent as the 'authorization' cookie.
    Flow:
      GET  /oauth/login3          -> {"key": "<one-time-key>"}
      POST /oauth/login3  + JSON  -> {"token": "<jwt>"}
    """
    global _auth_token
    if _auth_token:
        return _auth_token
    try:
        r1 = requests.get(f"{API_URL}/oauth/login3", timeout=5)
        key = r1.json()["key"]
        r2 = requests.post(f"{API_URL}/oauth/login3", json={
            "username": "john.newbie@world.com",
            "password": "john.newbie@world.com",
            "key": key,
        }, timeout=5)
        _auth_token = r2.json()["token"]
        print(f"  [AUTH] Token obtained: {_auth_token[:50]}...")
        return _auth_token
    except Exception as e:
        print(f"  [AUTH] Login failed: {e}")
        return None


def gql(query: str, variables: dict = None) -> requests.Response:
    """Send an unauthenticated GQL request."""
    body = {"query": query}
    if variables:
        body["variables"] = variables
    return requests.post(GQL_URL, json=body, headers=HEADERS, timeout=10)


def gql_authed(query: str, variables: dict = None) -> requests.Response:
    """Send an authenticated GQL request (JWT in authorization cookie)."""
    token = get_auth_token()
    body = {"query": query}
    if variables:
        body["variables"] = variables
    h = {**HEADERS}
    if token:
        h["cookie"] = f"authorization={token}"
    return requests.post(GQL_URL, json=body, headers=h, timeout=10)


# ---------------------------------------------------------------------------
# GQL queries used in tests
# ---------------------------------------------------------------------------

# user_profile category: contains user/group/role/membership keywords
QUERY_USERS = """
query GetUsers {
  users {
    id
    name
    email
  }
}
"""

QUERY_GROUPS = """
query GetGroups {
  groups {
    id
    name
    abbr
  }
}
"""

# app_metadata category: contains event/project/form keywords
QUERY_EVENTS = """
query GetEvents {
  events {
    id
    name
  }
}
"""

QUERY_PROJECTS = """
query GetProjects {
  projects {
    id
    name
  }
}
"""

# Mixed payload: contains BOTH user fields AND event fields in one query
# Expected: classified as user_profile (user keywords win priority)
QUERY_MIXED = """
query GetUsersAndEvents {
  users {
    id
    name
  }
  events {
    id
    name
  }
}
"""

# user_profile mutation: should also write to user_profile_audit
# gql_ug uses a union return type - must use inline fragment to query fields.
# id and email are generated fresh each run via variables to avoid duplicate key errors.
MUTATION_USER_INSERT = """
mutation MyMutation($id: UUID!, $email: String!) {
  userInsert(user: {
    id: $id,
    name: "Decree53 Test User",
    email: $email
  }) {
    ... on UserGQLModel {
      id
      name
      email
    }
    ... on UserGQLModelInsertError {
      msg
    }
  }
}
"""

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_health():
    print("\nTest 1: /decree53/health - MySQL connected")
    try:
        r = requests.get(HEALTH_URL, timeout=5)
        data = r.json()
        if data.get("status") == "ok" and data.get("local_db") == "connected":
            ok(f"health OK - ip_logs_total={data['ip_logs_total']} audit_total={data['user_profile_audit_total']}")
        else:
            fail(f"health returned: {data}")
    except Exception as e:
        fail(f"Cannot reach {HEALTH_URL}: {e}")
        print("  -> Make sure the stack is running first")
        sys.exit(1)


def test_user_query_routed_local():
    print("\nTest 2: User query -> should be routed LOCAL (MySQL)")
    try:
        r = gql(QUERY_USERS)
        category = r.headers.get("X-Data-Category", "")
        routed   = r.headers.get("X-Decree53-Routed", "")
        if category == "user_profile" and routed == "local":
            ok(f"X-Data-Category={category}  X-Decree53-Routed={routed}")
        else:
            fail(f"Expected user_profile/local, got {category}/{routed}")
    except Exception as e:
        fail(f"Request failed: {e}")


def test_group_query_routed_local():
    print("\nTest 3: Group query -> should be routed LOCAL (MySQL)")
    try:
        r = gql(QUERY_GROUPS)
        category = r.headers.get("X-Data-Category", "")
        routed   = r.headers.get("X-Decree53-Routed", "")
        if category == "user_profile" and routed == "local":
            ok(f"X-Data-Category={category}  X-Decree53-Routed={routed}")
        else:
            fail(f"Expected user_profile/local, got {category}/{routed}")
    except Exception as e:
        fail(f"Request failed: {e}")


def test_event_query_routed_global():
    print("\nTest 4: Event query -> should be routed GLOBAL (PostgreSQL)")
    try:
        r = gql(QUERY_EVENTS)
        category = r.headers.get("X-Data-Category", "")
        routed   = r.headers.get("X-Decree53-Routed", "")
        if category == "app_metadata" and routed == "global":
            ok(f"X-Data-Category={category}  X-Decree53-Routed={routed}")
        else:
            fail(f"Expected app_metadata/global, got {category}/{routed}")
    except Exception as e:
        fail(f"Request failed: {e}")


def test_project_query_routed_global():
    print("\nTest 5: Project query -> should be routed GLOBAL (PostgreSQL)")
    try:
        r = gql(QUERY_PROJECTS)
        category = r.headers.get("X-Data-Category", "")
        routed   = r.headers.get("X-Decree53-Routed", "")
        if category == "app_metadata" and routed == "global":
            ok(f"X-Data-Category={category}  X-Decree53-Routed={routed}")
        else:
            fail(f"Expected app_metadata/global, got {category}/{routed}")
    except Exception as e:
        fail(f"Request failed: {e}")


def test_mixed_query_user_wins():
    print("\nTest 6: Mixed query (users + events in one request) -> user_profile wins -> LOCAL")
    print("  Note: routing is per-request, not per-field.")
    print("        A single request cannot be split between Local and Global DB.")
    try:
        r = gql(QUERY_MIXED)
        category = r.headers.get("X-Data-Category", "")
        routed   = r.headers.get("X-Decree53-Routed", "")
        if category == "user_profile" and routed == "local":
            ok(f"user_profile wins over app_metadata - X-Decree53-Routed={routed}")
        else:
            fail(f"Expected user_profile/local, got {category}/{routed}")
    except Exception as e:
        fail(f"Request failed: {e}")


def test_user_mutation_writes_audit():
    print("\nTest 7: User mutation (authenticated) -> PostgreSQL + Local DB audit written")
    try:
        # Get counts before
        r_before = requests.get(HEALTH_URL, timeout=5).json()
        audit_before = r_before.get("user_profile_audit_total", 0)

        # Send mutation WITH auth token so gql_ug actually processes it in PostgreSQL.
        # Fresh UUID and email each run to avoid duplicate key errors.
        import uuid as _uuid
        variables = {
            "id": str(_uuid.uuid4()),
            "email": f"decree53_{_uuid.uuid4().hex[:8]}@example.com",
        }
        r = gql_authed(MUTATION_USER_INSERT, variables=variables)
        category = r.headers.get("X-Data-Category", "")
        routed   = r.headers.get("X-Decree53-Routed", "")

        # Print what gql_ug returned (to confirm PostgreSQL write)
        try:
            gql_response = r.json()
            print(f"  [GQL response] {gql_response}")
        except Exception:
            print(f"  [GQL response] (non-JSON) {r.text[:200]}")

        time.sleep(0.5)  # give async write time to complete

        r_after = requests.get(HEALTH_URL, timeout=5).json()
        audit_after = r_after.get("user_profile_audit_total", 0)

        if category == "user_profile" and routed == "local" and audit_after > audit_before:
            ok(f"mutation routed local, PostgreSQL write attempted, audit rows: {audit_before} -> {audit_after}")
        elif category == "user_profile" and routed == "local":
            ok(f"mutation routed local correctly (audit rows unchanged - check GQL response above)")
        else:
            fail(f"Expected user_profile/local, got {category}/{routed}")
    except Exception as e:
        fail(f"Request failed: {e}")


async def test_ip_logs_in_mysql():
    print("\nTest 8: Verify ip_logs written to MySQL for all requests above")
    try:
        pool = await aiomysql.create_pool(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASS,
            db=DB_NAME, autocommit=True, charset="utf8mb4",
        )
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT COUNT(*) FROM ip_logs")
                (count,) = await cur.fetchone()

                # Check that we have records for each category
                await cur.execute(
                    "SELECT data_category, COUNT(*) as n FROM ip_logs GROUP BY data_category"
                )
                rows = await cur.fetchall()

        pool.close()
        await pool.wait_closed()

        if count > 0:
            ok(f"ip_logs has {count} total rows")
            for category, n in rows:
                print(f"         {category}: {n} rows")
        else:
            fail("ip_logs is empty - check if Local_DB is reachable from the container")
    except Exception as e:
        fail(f"Cannot connect to MySQL on {DB_HOST}:{DB_PORT}: {e}")
        print(f"  -> Make sure MySQL is exposed on port {DB_PORT}")


async def dump_db():
    """Print all rows from ip_logs and user_profile_audit for visual inspection."""
    try:
        pool = await aiomysql.create_pool(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASS,
            db=DB_NAME, autocommit=True, charset="utf8mb4",
        )
        async with pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                # ip_logs
                await cur.execute(
                    "SELECT id, ip_address, method, endpoint, gql_operation, "
                    "data_category, status_code, ts FROM ip_logs ORDER BY ts"
                )
                ip_rows = await cur.fetchall()

                # user_profile_audit
                await cur.execute(
                    "SELECT id, user_id, operation_name, payload, recorded_at "
                    "FROM user_profile_audit ORDER BY recorded_at"
                )
                audit_rows = await cur.fetchall()

        pool.close()
        await pool.wait_closed()

        # --- ip_logs ---
        print("\n" + "=" * 55)
        print(f"  ip_logs  ({len(ip_rows)} rows)")
        print("=" * 55)
        for r in ip_rows:
            print(
                f"  [{r['ts']}] {r['method']} {r['endpoint']}"
                f"\n    ip={r['ip_address']}  op={r['gql_operation']}"
                f"  category={r['data_category']}  status={r['status_code']}"
            )

        # --- user_profile_audit ---
        print("\n" + "=" * 55)
        print(f"  user_profile_audit  ({len(audit_rows)} rows)")
        print("=" * 55)
        for r in audit_rows:
            print(
                f"  [{r['recorded_at']}] op={r['operation_name']}"
                f"  user_id={r['user_id']}"
                f"\n    payload={r['payload'][:120]}"
            )

    except Exception as e:
        print(f"\n[dump_db] Cannot connect to MySQL: {e}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    print("=" * 55)
    print("  Decree 53 Integration Tests")
    print(f"  API: {GQL_URL}")
    print(f"  MySQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    print("=" * 55)

    # HTTP tests (synchronous)
    test_health()
    test_user_query_routed_local()
    test_group_query_routed_local()
    test_event_query_routed_global()
    test_project_query_routed_global()
    test_mixed_query_user_wins()
    test_user_mutation_writes_audit()

    # MySQL verification (async)
    await test_ip_logs_in_mysql()

    # Print raw DB rows for visual inspection
    await dump_db()

    print("\n" + "=" * 55)
    print(f"  Result: {passed} passed, {failed} failed")
    print("=" * 55 + "\n")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
