import os
import asyncio
import jwt
import uuid
import aiohttp

from typing import Callable, Awaitable, Union
import fastapi
from fastapi import FastAPI, Request, status, Form, Header, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse, Response

def decodeJWTToken_sync(jwt_token):
    from jwt import PyJWKClient
    if isinstance(jwt_token, bytes):
        jwt_token = jwt_token.decode("utf-8")
    if not isinstance(jwt_token, str):
        raise ValueError("JWT token must be a string or bytes")

    # Ověření pomocí veřejného klíče z Azure
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    issuer = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
    jwks_url = f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"

    # Získání správného klíče pro podpis
    jwk_client = PyJWKClient(jwks_url)
    signing_key = jwk_client.get_signing_key_from_jwt(jwt_token)

    decoded = jwt.decode(
        jwt_token,
        signing_key.key,
        algorithms=["RS256"],
        audience=client_id,
        issuer=issuer,
        options={"verify_exp": True, "verify_aud": True, "verify_iss": True}
    )
    return decoded

async def decodeJWTToken(jwt_token):
    decoded_token = await asyncio.to_thread(decodeJWTToken_sync, jwt_token)
    return decoded_token
    


def createServer(
        iss="http://localhost:8000/publickey", 
        db_users=[{"id": "5563aa07-45c8-4098-af17-f2e8ec21b9df", "email": "someone@somewhere.world"}],
        passwordValidator: Callable[[str, str], Awaitable[bool]] = None,
        emailMapper: Callable[[str], Awaitable[str]] = None
        ):
    
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")


    app = FastAPI()

    server_metadata_url=f'https://login.microsoftonline.com/{os.getenv("AZURE_TENANT_ID")}/v2.0/.well-known/openid-configuration'

    simple_database = {}
    token_database = {}

    
    callbackuri = "/entra/auth"
    @app.get("/login")
    async def login(request: Request):
        callback_base_url = f"{request.url.scheme}://{request.url.netloc}"
        from urllib.parse import urlencode
        state = uuid.uuid4().hex  # Generuj bezpečný náhodný stav
        while state in simple_database:
            state = uuid.uuid4().hex
        params = request.query_params
        simple_database[state] = {
            "state": state,
            "redirect_uri": params.get("redirect_uri", "/"),
            "nonce": params.get("nonce", uuid.uuid4().hex)  # Přidání nonce pro bezpečnost
        }  # Ulož stav do jednoduché databáze
        # host = request.
        params = {
            "client_id": os.getenv("AZURE_CLIENT_ID"),
            "response_type": "code",
            "redirect_uri": f"{callback_base_url}{callbackuri}",
            "response_mode": "query",
            "scope": "openid profile email",
            "state": state
        }
        tenant_id = os.getenv("AZURE_TENANT_ID")
        authorize_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize?" + urlencode(params)
        return fastapi.responses.RedirectResponse(authorize_url)

    @app.route(callbackuri)
    async def auth(request: Request):
        params = request.query_params
        callback_base_url = f"{request.url.scheme}://{request.url.netloc}"
        # logging.info(f"/auth called")
        state = params.get("state")
        code = params.get("code")
        if not state or state not in simple_database:
            # return RedirectResponse(url="/login")
            state_data = {
                "state": state,
                "redirect_uri": "/",
                "nonce": uuid.uuid4().hex  # Přidání nonce pro bezpečnost
            }
            pass
        else:
            state_data = simple_database[state]
            if not state_data.get("redirect_uri"):
                state_data['redirect_uri'] = "/"
        if not code:
            return RedirectResponse(url="/")
        # logging.info(f"State: {state}, Code: {code}")
        # https://login.microsoftonline.com/organizations/oauth2/v2.0/token
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("AZURE_TENANT_ID")
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f"{callback_base_url}{callbackuri}"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(token_url, data=token_params) as entra_response:
                if entra_response.status != 200:
                    text = await entra_response.text()
                    # logging.error(f"Error fetching token: {entra_response.status} - {text}")
                    return RedirectResponse(url="/")
                token_data = await entra_response.json()
                # logging.info(f"got token_data: {token_data}")
                access_token = token_data.get("access_token")
                token_database[access_token] = {
                    "token_data": token_data
                }
                if not access_token:
                    # logging.info("auth.redirecting")
                    return RedirectResponse(url="/")
                result = RedirectResponse(url=state_data['redirect_uri'])
                cookie_setup = {
                    "key": "authorization",
                    "value": access_token,
                    "httponly": True,
                    "max_age": token_data.get("expires_in", 3600),  # Výchozí hodnota 1 hodina
                    "secure": True if request.url.scheme == "https" else False
                }
                result.set_cookie(**cookie_setup)
        return result
    
    @app.get("/logout")
    async def logout(request: Request):
        access_token = request.cookies.get("authorization")
        token_data = token_database.get(access_token)
        if not token_data:
            return RedirectResponse(url="/")
        del token_database[access_token]
        result = RedirectResponse(url="/")
        result.delete_cookie("authorization")
        # request.session.pop('user', None)
        return result    
    
    @app.get('/login2')
    async def getLoginPage(response_type: Union[str, None] = 'code', 
        client_id: Union[str, None] = 'SomeClientID', state: Union[str, None] = 'SomeState', redirect_uri: Union[str, None] = 'redirectURL'):
        return HTMLResponse("not supported")

    @app.post('/login2')
    async def postNameAndPassword(response: Response, username: str = Form(None), password: str = Form(None), key: str = Form(None)):
        return RedirectResponse(f"/login", status_code=status.HTTP_302_FOUND)
    
    @app.get('/login3')
    async def getLoginPage():
        device_code_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/devicecode"
        scope = "openid profile email offline_access"
        async with aiohttp.ClientSession() as session:
            async with session.post(device_code_url, data={
                "client_id": client_id,
                "scope": scope
            }) as resp: 
                result = await resp.json()
        return {
            "verification_uri": result["verification_uri"],
            "user_code": result["user_code"],
            "device_code": result["device_code"],
            "interval": result.get("interval", 5),
            "expires_in": result.get("expires_in", 900)
        }

    @app.get('/login3_device')
    async def getLoginPageDevice(device_code: str, interval: int = 5, timeout: int = 900):
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        elapsed = 0
        async with aiohttp.ClientSession() as session:
            while elapsed < timeout:
                await asyncio.sleep(interval)
                async with session.post(token_url, data={
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                    "client_id": client_id,
                    "device_code": device_code
                }) as token_resp:
                    text = await token_resp.text()
                    if token_resp.status == 200:
                        token_data = await token_resp.json()
                        return {
                            "message": "Autentizace hotova.",
                            "token": token_data
                        }
                    elif token_resp.status == 400 and "authorization_pending" in text:
                        print("Čekám na dokončení autorizace…")
                    else:
                        return {
                            "error": text
                        }
                elapsed += interval
        return {
            "error": "Timeout – uživatel nepotvrdil device code včas."
        }

    @app.post('/login3')
    async def postNameAndPasswordinJSON(response: Response):
        return {"error": "Not implemented"}

    @app.post('/login')
    async def postNameAndPassword(username: str = Form(None), password: str = Form(None), key: str = Form(None)):
        return {"error": "Not implemented"}

    @app.post('/token')
    async def exchangeCodeForToken(response: Response):
        return {"error": "Not implemented"}

    @app.get('/userinfo')
    async def getUserInfo(authorization: Union[str, None] = Header(default='Bearer _')):
        # return data from entra id
        # id should be set to oid
        pass

    @app.get('/logout')
    async def logout(authorization: Union[str, None] = Cookie(default='')):
        response = RedirectResponse(f"./login?redirect_uri=/")
        response.delete_cookie(key="authorization")
        return response

    @app.get('/logout2')
    async def logout(authorization: Union[str, None] = Header(default='Bearer _')):
        response = RedirectResponse(f"./login?redirect_uri=/")
        response.delete_cookie(key="authorization")
        return response

    @app.get('/publickey')
    async def getPublicKeyPem():
        # get publickey from entra and return it
        # return pem_public_key.decode('ascii')
