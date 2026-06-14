# bridge_app.py
"""
FastAPI bridge mezi easy_entra_id a Apollo Federation.

Použití:
    uvicorn bridge_app:app --host 0.0.0.0 --port 8000

Role tohoto souboru:
    1. easy_entra_id zůstává beze změny a předává ověřenou Entra identitu
       v hlavičkách x-ms-client-principal*.
    2. Tento bridge obsluhuje POST /api/gql.
    3. Z Entra hlaviček vytvoří interní JWT kompatibilní s dosavadním stackem.
    4. Interní JWT pošle v Authorization/Cookie vůči Apollo kontejneru.
    5. Odpověď z Apollo vrátí zpět klientovi.
    6. Ostatní endpointy vrací jedinou HTML debug stránku.
    7. Pro kompatibilitu se stávajícími gql službami vystavuje:
       - /oauth/publickey
       - /oauth/userinfo

Důležité bezpečnostní pravidlo:
    Tento kontejner nesmí být dostupný přímo z internetu.
    Musí být dostupný pouze přes easy_entra_id nebo interní Docker síť,
    protože důvěřuje x-ms-client-principal hlavičkám.
"""

from __future__ import annotations

import base64
import html
import json
import os
import time
import uuid
from typing import Any, Optional

from pathlib import Path
import httpx
from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from jose import jwt
from jose.exceptions import JWTError

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# ---------------------------------------------------------------------
# Konfigurace
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
INDEX_HTML_PATH = BASE_DIR / "index.html"
INDEX_HTML_PATH = os.getenv("INDEX_HTML_PATH", str(INDEX_HTML_PATH))
APP_TITLE = os.getenv("APP_TITLE", "Easy Entra ID → Apollo Bridge")

APOLLO_GQL_URL = os.getenv(
    "APOLLO_GQL_URL",
    "http://apollo:3000/api/gql/",
)

COOKIE_NAME = os.getenv("AUTH_COOKIE_NAME", "authorization")

INTERNAL_JWT_ISSUER = os.getenv(
    "INTERNAL_JWT_ISSUER",
    "frontend-bridge-internal-oauth",
)

INTERNAL_JWT_TTL_SECONDS = int(os.getenv("INTERNAL_JWT_TTL_SECONDS", "3600"))

# JSON mapování Entra uživatelů na lokální user id.
#
# Podporované tvary:
#   LOCAL_USER_MAP_JSON='{"john@world.com":"uuid-user-id"}'
#   LOCAL_USER_MAP_JSON='{"john@world.com":{"id":"uuid-user-id","name":"John","email":"john@world.com"}}'
#
# Pokud mapa neobsahuje uživatele, použije se fallback:
#   LOCAL_USER_DEFAULT_ID=...
#
# Pokud není ani fallback, vytvoří se stabilní uuid5 z Entra oid/email.
# To je použitelné pro demo, ale produkčně je lepší explicitní mapování
# na skutečné id uživatele ve vašem IS.
LOCAL_USER_MAP_JSON = os.getenv("LOCAL_USER_MAP_JSON", "{}")
LOCAL_USER_DEFAULT_ID = os.getenv("LOCAL_USER_DEFAULT_ID")

DEBUG_SHOW_RAW_PRINCIPAL = os.getenv("DEBUG_SHOW_RAW_PRINCIPAL", "false").lower() == "true"

HTTP_TIMEOUT_SECONDS = float(os.getenv("HTTP_TIMEOUT_SECONDS", "30"))


# ---------------------------------------------------------------------
# Interní JWT autorita
# ---------------------------------------------------------------------

class InternalJwtAuthority:
    def __init__(self) -> None:
        self.private_key_pem = self._load_or_create_private_key_pem()
        self.public_key_pem = self._public_key_from_private_key_pem(self.private_key_pem)

        # access_token -> {"user": ..., "exp": ...}
        # Pro jeden uvicorn worker je to OK.
        # Pro více workerů/replicas použij Redis/Valkey nebo deterministické userinfo.
        self.sessions: dict[str, dict[str, Any]] = {}

    def _load_or_create_private_key_pem(self) -> str:
        pem = os.getenv("INTERNAL_JWT_PRIVATE_KEY")
        if pem:
            return pem.replace("\\n", "\n")

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        return private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

    def _public_key_from_private_key_pem(self, private_key_pem: str) -> str:
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode("utf-8"),
            password=None,
        )

        return private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    def create_token(self, user: dict[str, Any]) -> tuple[str, int]:
        now = int(time.time())
        exp = now + INTERNAL_JWT_TTL_SECONDS
        access_token = str(uuid.uuid4())

        payload = {
            "iss": INTERNAL_JWT_ISSUER,
            "iat": now,
            "nbf": now,
            "exp": exp,

            # Kompatibilita s dosavadním BasicAuthBackend4Phase:
            # backend z JWT vyčte access_token a tím se ptá /oauth/userinfo.
            "access_token": access_token,

            # Užitečné interní claimy.
            "sub": str(user["id"]),
            "user_id": str(user["id"]),
            "email": user.get("email"),
            "name": user.get("name"),
        }

        token = jwt.encode(
            payload,
            self.private_key_pem,
            algorithm="RS256",
        )

        self.sessions[access_token] = {
            "user": user,
            "exp": exp,
        }

        return token, INTERNAL_JWT_TTL_SECONDS

    def get_user_by_access_token(self, access_token: str) -> Optional[dict[str, Any]]:
        session = self.sessions.get(access_token)

        if not session:
            return None

        if session["exp"] < int(time.time()):
            self.sessions.pop(access_token, None)
            return None

        return session["user"]

    def decode_internal_jwt(self, token: str) -> dict[str, Any]:
        return jwt.decode(
            token.removeprefix("Bearer ").strip(),
            self.public_key_pem,
            algorithms=["RS256"],
            options={
                "verify_aud": False,
            },
        )


authority = InternalJwtAuthority()


# ---------------------------------------------------------------------
# Entra principal helpers
# ---------------------------------------------------------------------

def _load_local_user_map() -> dict[str, Any]:
    try:
        value = json.loads(LOCAL_USER_MAP_JSON)
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


LOCAL_USER_MAP = _load_local_user_map()


def decode_x_ms_client_principal(value: str) -> dict[str, Any]:
    """
    easy_entra_id posílá x-ms-client-principal jako base64 JSON podobný Azure EasyAuth.
    """
    try:
        padded = value + "=" * (-len(value) % 4)
        raw = base64.b64decode(padded)
        return json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise ValueError(f"Invalid x-ms-client-principal header: {e}") from e


def claims_list_to_dict(principal: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}

    for claim in principal.get("claims", []):
        typ = claim.get("typ")
        val = claim.get("val")

        if typ:
            result[str(typ)] = val

    return result


def extract_entra_identity(request: Request) -> dict[str, Any]:
    principal_b64 = request.headers.get("x-ms-client-principal")
    principal_id = request.headers.get("x-ms-client-principal-id")
    principal_name = request.headers.get("x-ms-client-principal-name")

    if not principal_b64:
        raise ValueError("Missing x-ms-client-principal. Request probably bypassed easy_entra_id.")

    principal = decode_x_ms_client_principal(principal_b64)
    claims = claims_list_to_dict(principal)

    oid = (
        principal_id
        or claims.get("oid")
        or claims.get("sub")
        or claims.get("http://schemas.microsoft.com/identity/claims/objectidentifier")
    )

    email = (
        principal_name
        or claims.get("preferred_username")
        or claims.get("unique_name")
        or claims.get("email")
        or claims.get("upn")
        or claims.get("name")
    )

    name = claims.get("name") or email or oid

    if not oid and not email:
        raise ValueError("Cannot identify Entra user. Missing oid/sub/email/name claims.")

    return {
        "oid": str(oid) if oid else None,
        "email": str(email) if email else None,
        "name": str(name) if name else None,
        "claims": claims,
        "principal": principal,
    }


def map_entra_to_local_user(entra: dict[str, Any]) -> dict[str, Any]:
    """
    Mapování Entra identity na lokální user objekt očekávaný /oauth/userinfo.

    Produkčně doporučeno:
        LOCAL_USER_MAP_JSON='{"mail@domain.cz":"skutecne-uuid-v-is"}'

    Demo fallback:
        pokud mapování není nalezeno, vytvoří se stabilní uuid5.
    """
    email = entra.get("email")
    oid = entra.get("oid")
    name = entra.get("name") or email or oid

    map_keys = [
        email,
        email.lower() if isinstance(email, str) else None,
        oid,
    ]

    for key in map_keys:
        if not key:
            continue

        mapped = LOCAL_USER_MAP.get(key)
        if isinstance(mapped, str):
            return {
                "id": mapped,
                "email": email,
                "name": name,
                "entra_oid": oid,
            }

        if isinstance(mapped, dict) and mapped.get("id"):
            result = {
                "id": str(mapped["id"]),
                "email": mapped.get("email", email),
                "name": mapped.get("name", name),
                "entra_oid": oid,
            }
            return result

    if LOCAL_USER_DEFAULT_ID:
        return {
            "id": LOCAL_USER_DEFAULT_ID,
            "email": email,
            "name": name,
            "entra_oid": oid,
        }

    stable_source = f"entra:{oid or email}"
    return {
        "id": str(uuid.uuid5(uuid.NAMESPACE_URL, stable_source)),
        "email": email,
        "name": name,
        "entra_oid": oid,
    }


def sanitize_debug_headers(request: Request) -> dict[str, str]:
    safe_prefixes = (
        "x-ms-client-principal",
        "x-forwarded",
        "host",
        "user-agent",
        "content-type",
    )

    result = {}

    for key, value in request.headers.items():
        key_lower = key.lower()

        if key_lower in {"cookie", "authorization"}:
            result[key] = "[hidden]"
            continue

        if key_lower.startswith(safe_prefixes):
            if key_lower == "x-ms-client-principal" and not DEBUG_SHOW_RAW_PRINCIPAL:
                result[key] = "[present, hidden]"
            else:
                result[key] = value

    return result


# ---------------------------------------------------------------------
# FastAPI aplikace
# ---------------------------------------------------------------------

app = FastAPI(title=APP_TITLE)


@app.get("/health")
async def health():
    return {
        "ok": True,
        "service": "easy_entra_id_apollo_bridge",
        "apollo_gql_url": APOLLO_GQL_URL,
    }


@app.get("/oauth/publickey")
async def oauth_publickey():
    """
    Kompatibilní endpoint pro gql služby:
        JWTPUBLICKEYURL=http://frontend:8000/oauth/publickey
    """
    return Response(
        content=authority.public_key_pem,
        media_type="text/plain",
    )


@app.get("/oauth/userinfo")
async def oauth_userinfo(authorization: str = Header(default="")):
    """
    Kompatibilní endpoint pro gql služby:
        JWTRESOLVEUSERPATHURL=http://frontend:8000/oauth/userinfo

    Očekává:
        Authorization: Bearer <access_token>

    access_token je hodnota uložená uvnitř interního JWT.
    """
    if not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"detail": "Missing Bearer token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = authorization.split(" ", 1)[1]
    user = authority.get_user_by_access_token(access_token)

    if not user:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or expired access token"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "user": user,
    }


@app.post("/api/gql")
async def api_gql(request: Request):
    """
    Jediný aplikační API endpoint bridge.

    Vstup:
        Browser -> easy_entra_id -> tento frontend bridge
        easy_entra_id přidá x-ms-client-principal hlavičky.

    Výstup:
        Tento bridge vytvoří interní JWT a pošle požadavek do Apollo:
            Authorization: Bearer <internal_jwt>
            Cookie: authorization=<internal_jwt>
    """
    try:
        entra = extract_entra_identity(request)
        local_user = map_entra_to_local_user(entra)
        internal_jwt, max_age = authority.create_token(local_user)
    except ValueError as e:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Unauthenticated",
                "reason": str(e),
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    body = await request.body()

    # Minimalistické předávání hlaviček: do Apollo nejde x-ms principal,
    # ale pouze interní JWT, kterému rozumí dosavadní federace.
    outgoing_headers = {
        "content-type": request.headers.get("content-type", "application/json"),
        "accept": request.headers.get("accept", "application/json"),
        # "authorization": f"Bearer {internal_jwt}",
        "cookie": f"{COOKIE_NAME}={internal_jwt}",
        "x-forwarded-user": str(local_user.get("id")),
        "x-forwarded-user-email": str(local_user.get("email") or ""),
        "x-auth-bridge": "easy_entra_id_apollo_bridge",
    }

    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SECONDS, follow_redirects=False) as client:
            print(f"Forwarding request to Apollo: {APOLLO_GQL_URL} with headers: \n{outgoing_headers}\nBody: {body.decode('utf-8')}")
            apollo_response = await client.post(
                APOLLO_GQL_URL,
                content=body,
                headers=outgoing_headers,
            )
    except httpx.RequestError as e:
        print(f"Apollo request failed: {e}")
        return JSONResponse(
            status_code=502,
            content={
                "detail": "Apollo request failed",
                "apollo_gql_url": APOLLO_GQL_URL,
                "reason": str(e),
            },
        )

    excluded_headers = {
        "connection",
        "content-encoding",
        "transfer-encoding",
        "set-cookie",
    }

    response_headers = {
        key: value
        for key, value in apollo_response.headers.items()
        if key.lower() not in excluded_headers
    }

    response = Response(
        content=apollo_response.content,
        status_code=apollo_response.status_code,
        headers=response_headers,
        media_type=apollo_response.headers.get("content-type", "application/json"),
    )

    # Volitelné: klient dostane interní JWT cookie.
    # Není nutná pro bezpečnost bridge, protože další request opět projde přes easy_entra_id,
    # ale hodí se pro debug a kompatibilitu s browser chováním.
    response.set_cookie(
        key=COOKIE_NAME,
        value=internal_jwt,
        httponly=True,
        max_age=max_age,
        secure=request.url.scheme == "https",
        samesite="lax",
    )

    return response


def build_debug_html(request: Request) -> str:
    try:
        entra = extract_entra_identity(request)
        local_user = map_entra_to_local_user(entra)
        auth_state = "authenticated"
    except Exception as e:
        entra = None
        local_user = None
        auth_state = f"not authenticated: {e}"

    debug_payload = {
        "appTitle": APP_TITLE,
        "authState": auth_state,
        "path": str(request.url.path),
        "apolloGqlUrl": APOLLO_GQL_URL,
        "cookieName": COOKIE_NAME,
        "internalJwtIssuer": INTERNAL_JWT_ISSUER,
        "headers": sanitize_debug_headers(request),
        "entra": {
            "oid": entra.get("oid"),
            "email": entra.get("email"),
            "name": entra.get("name"),
            "claims": entra.get("claims"),
        } if entra else None,
        "localUser": local_user,
        "notes": [
            "POST /api/gql vytvoří interní JWT z Entra hlaviček a pošle GraphQL request do Apollo.",
            "GET /oauth/publickey a GET /oauth/userinfo jsou kompatibilní endpointy pro stávající gql služby.",
            "Všechny ostatní cesty vrací tuto jedinou HTML stránku.",
        ],
    }

    debug_json = json.dumps(debug_payload, ensure_ascii=False, indent=2)

    # Pozor: obsah <script> je raw text, HTML entities jako &quot; se v něm
    # nepřevedou zpět na uvozovky. Proto nepoužívat html.escape(debug_json).
    # Escapujeme jen znaky nebezpečné pro ukončení / rozbití script tagu.
    debug_json_for_script = (
        debug_json
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )
    try:
        html_content = open(INDEX_HTML_PATH, "r", encoding="utf-8").read()
        html_content = html_content.replace('"__DEBUG_DATA_PLACEHOLDER__"', debug_json_for_script)
    except FileNotFoundError:
        html_content = f"""
        <html>
        <head><title>{APP_TITLE} - Debug</title></head>
            <body>
                <h1>{APP_TITLE} - Debug</h1>
                <pre>{html.escape(debug_json)}</pre>
                <p>Note: index.html not found at {INDEX_HTML_PATH}</p>
            </body>
            </html>"""
    
    return html_content

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
async def spa_fallback(request: Request, path: str):
    """
    Vše kromě explicitních rout výše vrací jednu HTML stránku.
    Tím pádem /, /abc, /app/whatever i omylem zavolané endpointy zobrazí debug SPA.
    """
    return HTMLResponse(build_debug_html(request))
