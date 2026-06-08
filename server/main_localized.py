"""
main_localized.py  -  Decree 53 entry point
============================================
Copy of main.py with three changes:
  1. Imports gqlproxy_localized instead of gqlproxy
  2. Lifespan initializes the MySQL pool on startup
  3. Adds GET /decree53/health endpoint

Original main.py is NOT modified.
"""

import logging
import os
import asyncio
import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, RedirectResponse, HTMLResponse
from contextlib import asynccontextmanager

from mockoauthserver import server as OAuthServer

from .users import (
    ComposeConnectionString,
    startEngine, initDB,
    getDemoData, passwordValidator, emailMapper
)

from .data_router import init_pool, close_pool, get_pool

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d\t%(levelname)s:\t%(message)s',
    datefmt='%Y-%m-%dT%I:%M:%S')

connectionString = ComposeConnectionString()


def singleCall(asyncFunc):
    resultCache = {}
    async def result():
        if resultCache.get("result", None) is None:
            resultCache["result"] = await asyncFunc()
        return resultCache["result"]
    return result


@singleCall
async def RunOnceAndReturnSessionMaker():
    makeDrop = os.getenv("DEMO", None) in ["True", True]
    logging.info(f'starting engine for "{connectionString} makeDrop={makeDrop}"')
    asyncSessionMaker = await startEngine(
        connectionstring=connectionString, makeDrop=makeDrop, makeUp=True
    )
    logging.info("initializing system structures")
    asyncio.create_task(initDB(asyncSessionMaker))
    logging.info("all done")
    return asyncSessionMaker


DEMO = os.getenv("DEMO", None)
assert DEMO is not None, "DEMO environment variable must be explicitly defined"
assert (DEMO == "True") or (DEMO == "False"), "DEMO environment variable can have only `True` or `False` values"
DEMO = DEMO == "True"

if DEMO:
    logging.info("RUNNING IN DEMO MODE")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize PostgreSQL (credentials DB)
    await RunOnceAndReturnSessionMaker()

    # Initialize MySQL Local_DB (Decree 53)
    ok = await init_pool()
    if not ok:
        logging.warning(
            "[Decree53] Local_DB not ready - ip_log writes will be skipped until MySQL is reachable"
        )
    yield

    await close_pool()


app = FastAPI(lifespan=lifespan)

from .appindex import createIndexResponse
from uoishelpers.authenticationMiddleware import BasicAuthenticationMiddleware302, BasicAuthBackend
from .BasicAuthBackend4Phase import BasicAuthBackend4Phase as BasicAuthBackend

JWTPUBLICKEY = os.environ.get("JWTPUBLICKEY", "http://localhost:8000/oauth/publickey")
JWTRESOLVEUSERPATH = os.environ.get("JWTRESOLVEUSERPATH", "http://localhost:8000/oauth/userinfo")

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app, metric_namespace="frontnend").expose(app, endpoint="/metrics")

import json

configFile = "config.json"
dirName = ""
if __file__:
    dirName = os.path.dirname(__file__)

print("executing in", dirName)
configFile = dirName + "/" + configFile

# ---------------------------------------------------------------------------
# Stub out server.main in sys.modules so that appindex.py's lazy imports
#   from .main import configFile, dirName
# do NOT trigger main.py's module-level side effects (Prometheus metric
# registration via connectProxy, etc.).  Without this stub the Prometheus
# collector would be registered twice, raising:
#   ValueError: Duplicated timeseries in CollectorRegistry: gqlquery_processing_seconds
# ---------------------------------------------------------------------------
import sys as _sys
import types as _types
_main_stub = _types.ModuleType("server.main")
_main_stub.dirName = dirName
_main_stub.configFile = configFile
_sys.modules["server.main"] = _main_stub


def createApp(key, setup):
    file = setup["file"]
    subApp = FastAPI()

    @subApp.get("/{file_path:path}")
    async def getFile(file_path: str):
        filename = dirName + "/htmls/" + file
        if os.path.isfile(filename):
            return FileResponse(filename)
        else:
            return RedirectResponse("/")

    if not DEMO:
        subApp.add_middleware(BasicAuthenticationMiddleware302,
                              backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY,
                                                       JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
    app.mount("/" + key, subApp)


with open(configFile, "r", encoding="utf-8") as f:
    config = json.load(f)
    for key, setup in config.items():
        createApp(key, setup)


@app.get("/logout")
def logout():
    result = RedirectResponse("/oauth/login2?redirect_uri=/", status_code=303)
    result.delete_cookie("authorization")
    return result


demoData = getDemoData()
users = demoData.get("users", [])


async def bindedPasswordValidator(email, password):
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
    return await passwordValidator(asyncSessionMaker, email, password)


async def bindedEmailMapper(email):
    asyncSessionMaker = await RunOnceAndReturnSessionMaker()
    return await emailMapper(asyncSessionMaker, email)


db_users = [{"id": user["id"], "email": user["email"]} for user in users]
app.mount("/oauth", OAuthServer.createServer(
    db_users=db_users,
    passwordValidator=bindedPasswordValidator,
    emailMapper=bindedEmailMapper
))

# ---------------------------------------------------------------------------
# Decree 53 health endpoint  GET /decree53/health
# No auth required - used for monitoring and testing
# ---------------------------------------------------------------------------

decree53App = FastAPI()


@decree53App.get("/health")
async def decree53_health():
    """Check MySQL Local_DB connectivity and return row counts."""
    pool = await get_pool()
    if pool is None:
        return {"status": "error", "local_db": "unreachable"}
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT COUNT(*) FROM ip_logs")
                (ip_count,) = await cur.fetchone()
                await cur.execute("SELECT COUNT(*) FROM user_profile_audit")
                (audit_count,) = await cur.fetchone()
        return {
            "status": "ok",
            "local_db": "connected",
            "ip_logs_total": ip_count,
            "user_profile_audit_total": audit_count,
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}


app.mount("/decree53", decree53App)

# ---------------------------------------------------------------------------
# GQL proxy  (only change vs main.py: import from gqlproxy_localized)
# ---------------------------------------------------------------------------

apiApp = FastAPI()
if not DEMO:
    apiApp.add_middleware(BasicAuthenticationMiddleware302,
                          backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY,
                                                   JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
app.mount("/api", apiApp)

from .gqlproxy_localized import connectProxy   # <- only difference from main.py
connectProxy(apiApp)

# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------

debugApp = FastAPI()


@debugApp.get("/")
async def hello(requets: Request):
    import jwt
    cookies = requets.cookies
    bearer = cookies.get("authorization")
    token = bearer.replace("Bearer ", "")
    JWTPUBLICKEYURL = "http://127.0.0.1:8000/oauth/publickey"
    async with aiohttp.ClientSession() as session:
        async with session.get(JWTPUBLICKEYURL) as resp:
            assert resp.status == 200
            pktext = await resp.text()
    pkey = pktext.replace('"', "").replace("\\n", "\n")
    jwtdecoded = jwt.decode(jwt=token, key=pkey, algorithms=["RS256"])
    return {"hello": "world", "userid": jwtdecoded["user_id"]}


if not DEMO:
    debugApp.add_middleware(BasicAuthenticationMiddleware302,
                            backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY,
                                                     JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))
app.mount("/debug", debugApp)

# ---------------------------------------------------------------------------
# Generic SPA
# ---------------------------------------------------------------------------

genericsApp = FastAPI()
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "htmls/dyn"
INDEX_HTML = DIST_DIR / "index.html"


@genericsApp.get("/{full_path:path}")
async def so(full_path: str):
    candidate = DIST_DIR / full_path
    if candidate.exists() and candidate.is_file():
        return FileResponse(candidate)
    return FileResponse(INDEX_HTML)


app.mount("/generic", genericsApp)
if not DEMO:
    genericsApp.add_middleware(BasicAuthenticationMiddleware302,
                               backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY,
                                                        JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))

# ---------------------------------------------------------------------------
# Index portal
# ---------------------------------------------------------------------------

indexApp = FastAPI()


@indexApp.get("/")
async def index(request: Request):
    return await createIndexResponse(request=request)


app.mount("/index", indexApp)
if not DEMO:
    indexApp.add_middleware(BasicAuthenticationMiddleware302,
                            backend=BasicAuthBackend(JWTPUBLICKEY=JWTPUBLICKEY,
                                                     JWTRESOLVEUSERPATH=JWTRESOLVEUSERPATH))

# ---------------------------------------------------------------------------
# Analytics proxy
# ---------------------------------------------------------------------------

analyticsApp = FastAPI()


@analyticsApp.get("/{file_path:path}/")
async def analytics(file_path, request: Request):
    headers = dict(request.headers)
    query_params = request.query_params
    fullurl = request.url.include_query_params(**query_params)
    path = request.url.path
    fulluri = path + f"{fullurl}".split(request.url.path)[1]
    remoteurl = f"http://analytics:8000{fulluri}"
    try:
        del headers["host"]
        async with aiohttp.ClientSession() as session:
            async with session.get(remoteurl, headers=headers) as resp:
                text = await resp.text()
    except Exception as e:
        print("except", e)
    return HTMLResponse(content=text, status_code=resp.status)


app.mount("/analysis", analyticsApp)

# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------

@app.get("/")
async def root(request: Request):
    return RedirectResponse("/index", status_code=302)
