import logging
import pytest

serversTestscope = "function"

@pytest.fixture(scope=serversTestscope)
def DemoData():
    import server.users     
    return server.users.getDemoData()

@pytest.fixture
def AdminToken(DemoData, Token):
    users = DemoData["users"]
    user0 = users[0]
    token = Token(user0["email"], user0["email"])
    return token


@pytest.fixture
def Token(FastAPIClient):
    # users = DemoData["users"]
    # user0 = users[0]

    loginurl = '/oauth/login3'

    def GetToken(username, password):
        resp = FastAPIClient.get(loginurl)
        assert resp.status_code == 200, resp
        accessjson = resp.json()
        logging.info(f"keyjson {accessjson}")

        payload = {
            "username": username,
            "password": password,
            **accessjson
        }
        logging.info(f"payload {payload}")
        resp = FastAPIClient.post(loginurl, json=payload)
        assert resp.status_code == 200, resp
        logging.info(f"resp {resp.text}")
        tokendict = resp.json()
        token = tokendict["token"] 
        logging.info(f"have token {token}")
        # return
        return token

    return GetToken
    
@pytest.fixture
def FastAPIClient(SetSalt):
    from fastapi.testclient import TestClient
    import server.main

    server.main.connectionString = "sqlite+aiosqlite:///:memory:"   

    client = TestClient(server.main.app, raise_server_exceptions=False)   
    return client
    # def AcceptHeaders(AuthorizationHeaders):
    #     async def Execute(query, variable_values={}):
    #         json = {
    #             "query": query,
    #             "variables": variable_values
    #         }
    #         headers = AuthorizationHeaders
    #         logging.debug(f"query client for {query} with {variable_values} and headers {headers}")

    #         response = client.post("/gql", headers=headers, json=json)
    #         # assert response.status_code == 200, f"Got no 200 response {response}"
    #         return response.json()       
    #     return Execute
    # return AcceptHeaders

@pytest.fixture
def Publickey(FastAPIClient):

    response = FastAPIClient.get("/oauth/publickey")
    strkey = response.text
    strkey = strkey.replace('\\n', '\n').replace('"', '')
    logging.info(f"having key \n{strkey}")
    yield strkey

    # from fastapi.testclient import TestClient
    # import server.main
    # def ComposeCString():
    #     return "sqlite+aiosqlite:///:memory:"   
    # server.main.ComposeConnectionString = ComposeCString

    # client = TestClient(server.main.app, raise_server_exceptions=False)   
    # return client

@pytest.fixture
def DemoTrue(monkeypatch):
    print("setting env DEMO to True")
    monkeypatch.setenv("DEMO", "True")
    # import main
    # main.DEMO = True
    yield
    print("end of setting env DEMO to True")

@pytest.fixture
def DemoFalse(monkeypatch):
    print("setting env DEMO to False")
    monkeypatch.setenv("DEMO", "False")
    # import main
    # main.DEMO = True
    yield
    print("end of setting env DEMO to False")


@pytest.fixture
def SetSalt(monkeypatch):
    SALT = "fe1c71b2-74c0-41e5-978f-eecbffac7418"
    logging.info(f"SALT {SALT}")
    monkeypatch.setenv("SALT", "fe1c71b2-74c0-41e5-978f-eecbffac7418")
    # import main
    # main.DEMO = True
    yield

    