"""
gqlproxy_localized.py
Copy of gqlproxy.py with Decree 53 routing hooks added after each request.
Original gqlproxy.py is NOT modified.
"""

import os
import aiohttp
from fastapi.responses import JSONResponse, FileResponse
from fastapi import Request
from pydantic import BaseModel

from .prometheus import collectTime
from .data_router import DataRouter


class Item(BaseModel):
    query: str
    variables: dict = None
    operationName: str = None


def connectProxy(app):

    proxy = os.environ.get("GQL_PROXY", "http://10.0.2.27:33001/gql")
    print("using proxy", proxy)

    @app.get("/gql", response_class=FileResponse)
    async def apigql_get():
        realpath = os.path.realpath("./pyserver/graphiql.html")
        return realpath

    @app.get("/doc", response_class=FileResponse)
    async def apidoc_get():
        realpath = os.path.realpath("./pyserver/voyager.html")
        return realpath

    @collectTime("gqlquery")
    @app.post("/gql", response_class=JSONResponse)
    async def apigql_post(data: Item, request: Request):
        print(data, flush=True)

        # Build the query body to forward to Apollo
        gqlQuery = {}
        if data.operationName is not None:
            gqlQuery["operationName"] = data.operationName
        gqlQuery["query"] = data.query
        if data.variables is not None:
            gqlQuery["variables"] = data.variables

        # Forward auth headers to upstream - only include headers that are present.
        # aiohttp raises TypeError if a header value is None.
        c = dict(request.headers.items())
        out_headers = {}
        if c.get("cookie"):
            out_headers["cookie"] = c["cookie"]
        if c.get("authorization"):
            out_headers["authorization"] = c["authorization"]
        if c.get("Authorization"):
            out_headers["Authorization"] = c["Authorization"]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(proxy, json=gqlQuery, headers=out_headers) as resp:
                    upstream_status = resp.status
                    try:
                        # content_type=None: parse regardless of Content-Type header
                        json_body = await resp.json(content_type=None)
                    except Exception as json_err:
                        # Apollo returned non-JSON (e.g. startup HTML error page)
                        raw = await resp.text()
                        json_body = {
                            "errors": [{"message": f"Upstream returned non-JSON (status {upstream_status}): {raw[:300]}"}]
                        }
                        upstream_status = 502
        except aiohttp.ClientError as conn_err:
            # Apollo is not reachable (DNS failure, connection refused, etc.)
            return JSONResponse(
                content={"errors": [{"message": f"Cannot reach GQL proxy at {proxy}: {conn_err}"}]},
                status_code=502,
            )

        # --- Decree 53: classify and write to Local_DB ---
        client_ip = request.client.host if request.client else "unknown"
        user_agent = c.get("user-agent", "")
        user_id = None
        if hasattr(request.state, "user") and request.state.user:
            user_id = request.state.user.get("id")

        category = await DataRouter.process(
            query=data.query,
            variables=data.variables,
            request_ip=client_ip,
            endpoint="/api/gql",
            method="POST",
            user_agent=user_agent,
            user_id=user_id,
            status_code=upstream_status,
        )

        # Attach routing info to response headers for inspection
        response = JSONResponse(content=json_body, status_code=upstream_status)
        response.headers["X-Data-Category"] = category
        response.headers["X-Decree53-Routed"] = "local" if category == "user_profile" else "global"
        return response
